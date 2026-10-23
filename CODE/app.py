"""Gestión de alto nivel, independiente de network/."""
from queue import Queue,Empty
import sys
from pathlib import Path
import customtkinter as ctk
import button_actions
from styles.theme import THEME as T
from ui.layout import MainView
from interface_values import interface_values
from receiver_monitor import ReceiverMonitor
class App(ctk.CTk):
    def __init__(self, values=None):
        ctk.set_appearance_mode('light')
        ctk.set_widget_scaling(1)
        ctk.set_window_scaling(1)
        if sys.platform == 'win32':
            import ctypes
            # Declarar el DPI antes de crear Tk evita la ampliación borrosa de Windows.
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('InteligentCactus.Desktop')
        super().__init__()
        icon = Path(__file__).resolve().parents[1] / 'assets' / 'cactus-smooth.ico'
        if sys.platform == 'win32':
            self.iconbitmap(str(icon))
        self.title('Inteligent Cactus')
        width, height = T['width'], T['height']
        self.geometry(f'{width}x{height}')
        self.resizable(False,False)
        self.configure(fg_color=T['background'])
        self.values = interface_values if values is None else values
        self._last_values_version = -1
        self.connection_events=Queue()
        self.view=MainView(
            self,
            lambda: self.run_button_action('demo'),
            lambda: self.run_button_action('clear'),
            button_texts={key: item['text'] for key, item in button_actions.BUTTONS.items()},
        )
        self._render_values()
        # Centrar con las dimensiones físicas después de aplicar el DPI nativo.
        self.update_idletasks()
        x = max(0, (self.winfo_screenwidth() - self.winfo_width()) // 2)
        y = max(0, (self.winfo_screenheight() - self.winfo_height() - 64) // 2)
        self.geometry(f'+{x}+{y}')
        self.protocol('WM_DELETE_WINDOW',self.close)
        self._poll_id=self.after(150,self._poll)
        self.receiver_monitor = ReceiverMonitor(self.connection_events.put)
        self.receiver_monitor.start()
    def run_button_action(self, button_id):
        try:
            return button_actions.execute(button_id, self)
        finally:
            self._render_values()

    def submit_readings(self, values):
        """Compatibilidad con el receptor: un paquete reemplaza la lectura completa."""
        self.values.update(values, replace=True)

    def _render_values(self):
        version, values, source, timestamp = self.values.snapshot()
        if version == self._last_values_version:
            return
        self._last_values_version = version
        self.view.panel.update_values(values, timestamp.strftime('%H:%M:%S') if timestamp else '—')
        if source == 'demo':
            self.view.panel.updated.configure(text='Demo · datos simulados')
        elif source in ('clear', 'initial'):
            self.view.panel.updated.configure(text='')

    def _poll(self):
        state = None
        for _ in range(100):
            try:
                state = self.connection_events.get_nowait()
            except Empty:
                break
        if state is not None:
            self.view.status.set_state(state)
        self._render_values()
        self._poll_id=self.after(150,self._poll)

    def show_demo(self):
        self.values.demo()
        self._render_values()

    def clear_readings(self):
        self.values.clear()
        self._render_values()

    def close(self):
        self.after_cancel(self._poll_id)
        self.receiver_monitor.stop()
        self.destroy()
