"""Observa el receptor existente sin importar ni modificar network/receiver.py."""
import os
from pathlib import Path
import subprocess
import sys
import threading


class ReceiverMonitor:
    def __init__(self, on_state):
        self.on_state = on_state
        self.process = None
        self._stopping = threading.Event()

    def start(self):
        receiver = Path(__file__).resolve().parent / 'network' / 'receiver.py'
        try:
            self.process = subprocess.Popen(
                [sys.executable, '-u', str(receiver)], cwd=str(receiver.parent.parent),
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                text=True, encoding='utf-8', errors='replace',
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
            )
        except OSError:
            self.on_state('unavailable')
            return
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        connected = False
        with self.process.stdout as output:
            for line in output:
                if self._stopping.is_set():
                    return
                if line.startswith('ESP32 conectado:'):
                    connected = True
                    self.on_state('connected')
                elif line.startswith('ESP32 desconectado.'):
                    self.on_state('disconnected')
                elif line.startswith('Esperando al ESP32'):
                    self.on_state('waiting')
        self.process.wait()
        if not self._stopping.is_set():
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
