"""Gestión de alto nivel, independiente de network/."""
from datetime import datetime
from queue import Queue,Empty
import math
import sys
from pathlib import Path
import customtkinter as ctk
from styles.theme import THEME as T
from ui.layout import MainView
from ui.data_panel import SENSORS
from receiver_monitor import ReceiverMonitor
class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode('light')
        ctk.set_widget_scaling(1)
        ctk.set_window_scaling(1)
        if sys.platform == 'win32':
            import ctypes
            # Declarar el DPI antes de crear Tk evita la ampliación borrosa de Windows.
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('InteligentCactus.Desktop')
        super().__init__()
        icon = Path(__file__).resolve().parents[1] / 'assets' / 'cactus.ico'
        if sys.platform == 'win32':
            self.iconbitmap(str(icon))
        self.title('Inteligent Cactus')
        width, height = T['width'], T['height']
        self.geometry(f'{width}x{height}')
        self.resizable(False,False)
        self.configure(fg_color=T['background'])
        self.incoming=Queue()
        self.connection_events=Queue()
        self.view=MainView(self,self.show_demo,self.clear_readings)
        # Centrar con las dimensiones físicas después de aplicar el DPI nativo.
        self.update_idletasks()
        x = max(0, (self.winfo_screenwidth() - self.winfo_width()) // 2)
        y = max(0, (self.winfo_screenheight() - self.winfo_height() - 64) // 2)
        self.geometry(f'+{x}+{y}')
        self.protocol('WM_DELETE_WINDOW',self.close)
        self._poll_id=self.after(150,self._poll)
        self.receiver_monitor = ReceiverMonitor(self.connection_events.put)
        self.receiver_monitor.start()
    def submit_readings(self,values):
        """Integración futura: admite llamadas desde el hilo receptor."""
        clean={}
        for key,*_ in SENSORS:
            value=values.get(key)
            if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value)):
                raise ValueError(f'Lectura inválida: {key}')
            clean[key]=value
        self.incoming.put(clean)
    def _poll(self):
        state = None
        for _ in range(100):
            try:
                state = self.connection_events.get_nowait()
            except Empty:
                break
        if state is not None:
            self.view.status.set_state(state)
        latest=None
        for _ in range(100):
            try: latest=self.incoming.get_nowait()
            except Empty: break
        if latest is not None:
            self.view.panel.update_values(latest,datetime.now().strftime('%H:%M:%S'))

        self._poll_id=self.after(150,self._poll)
    def _drain(self):
        while True:
            try: self.incoming.get_nowait()
            except Empty: break
    def show_demo(self):
        self._drain()
        values=dict(zip((s[0] for s in SENSORS),(18,24.6,42,12500,22.8)))
        self.view.panel.update_values(values,datetime.now().strftime('%H:%M:%S'))
        self.view.panel.updated.configure(text='Demo · datos simulados')
    def clear_readings(self):
        self._drain()
        self.view.panel.update_values({},'—')
        self.view.panel.updated.configure(text='')

    def close(self):
        self.after_cancel(self._poll_id)
        self.receiver_monitor.stop()
        self.destroy()
