"""Inicia recibir.py y pasa su estado y sus medidas a la app."""
import os
import json
from pathlib import Path
import subprocess
import sys
import threading


class ReceiverMonitor:
    def __init__(self, on_state, on_readings=None):
        self.on_state = on_state
        self.on_readings = on_readings
        self.process = None
        self._stopping = threading.Event()
        self._thread = None

    def start(self):
        # Una pulsacion repetida nunca debe abrir dos receptores.
        if self.process is not None and self.process.poll() is None:
            return
        self.stop()
        self._stopping = threading.Event()
        if getattr(sys, 'frozen', False):
            receiver = Path(sys.executable).parent / 'recibir.py'
            command = [sys.executable, '--receptor']
        else:
            receiver = Path(__file__).resolve().parent.parent / 'recibir.py'
            command = [sys.executable, '-u', str(receiver)]
        try:
            self.process = subprocess.Popen(
                command, cwd=str(receiver.parent),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                text=True, encoding='utf-8', errors='replace',
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
            )
        except OSError:
            self.on_state('unavailable')
            return
        self._thread = threading.Thread(
            target=self._read, args=(self.process, self._stopping), daemon=True)
        self._thread.start()

    def _read(self, process, stopping):
        connected = False
        with process.stdout as output:
            for line in output:
                if stopping.is_set():
                    return
                print(line.rstrip(), flush=True)
                if line.startswith('ESP32 conectado:'):
                    connected = True
                    self.on_state('connected')
                elif line.startswith('ESP32 desconectado.'):
                    self.on_state('disconnected')
                elif line.startswith('Esperando al ESP32'):
                    self.on_state('waiting')
                elif line.startswith('Datos recibidos: ') and self.on_readings:
                    try:
                        datos = json.loads(line.removeprefix('Datos recibidos: '))
                        # Traducimos las claves del ESP32 a las claves de la app.
                        self.on_readings({
                            'air_temperature': datos['ta'],
                            'soil_temperature': datos['ts'],
                            'air_humidity': datos['ha'],
                            'soil_moisture': datos['hs'],
                            'light': datos['luz'],
                        })
                    except (ValueError, KeyError, TypeError) as error:
                        print('Medida no valida para la app:', error, flush=True)
        process.wait()
        if not stopping.is_set():
            self.on_state('disconnected' if connected else 'unavailable')

    def stop(self):
        self._stopping.set()
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=2)

        # Esperar al lector evita callbacks de una conexion que ya se ha cerrado.
        if self._thread is not None and self._thread is not threading.current_thread():
            self._thread.join(timeout=2)
