"""Ventana vertical: imagen central grande y valores a ambos lados."""
from paths import ASSETS_DIR
import customtkinter as ctk
from PIL import Image, ImageOps
from ui.theme import THEME as T
from ui.components import AppLabel, AppButton, ConnectionIndicator
from ui.data_panel import DataPanel

SENSOR_POSITIONS = {
    'air_temperature': (8, 214, 'Aire'),
    'air_humidity': (8, 332, 'Aire'),
    'soil_temperature': (8, 500, 'Suelo'),
    'light': (478, 175, 'Luz'),
    'soil_moisture': (478, 490, 'Suelo'),
}

class MainView:
    def __init__(self, root, on_connect, on_clear, button_texts):
        asset = ASSETS_DIR / 'cactus-limon-pastel.png'
        # Ajuste de encuadre solo en memoria: se conserva intacto el PNG original.
        with Image.open(asset) as source:
            display = ImageOps.fit(source.convert('RGB'), (T['width'] * 2, T['height'] * 2),
                                   method=Image.Resampling.LANCZOS)
        # Una misma escala para imagen, posiciones, cajas y texto.
        self.image = ctk.CTkImage(light_image=display, dark_image=display,
                                 size=(T['width'], T['height']))
        self.background = ctk.CTkLabel(root, text='', image=self.image,
                                      width=T['width'], height=T['height'], corner_radius=0)
        self.background.place(x=0, y=0)
        AppLabel(root, 'Inteligent CACTUS', size=25, weight='bold', height=36).place(
            relx=0.5, y=37, anchor='n')
        self.status = ConnectionIndicator(root)
        self.status.place(relx=1.0, x=-18, y=T['height'] - 34, anchor='ne')
        self.panel = DataPanel(root, SENSOR_POSITIONS)
        self.panel.updated.place_configure(relx=0, x=18, anchor='nw')
        self.connection_button = AppButton(root, text=button_texts['connect'], command=on_connect, width=144)
        self.connection_button.place(x=184, y=T['height'] - 82)
        self.clear_button = AppButton(root, text=button_texts['clear'], command=on_clear, width=128, variant='secondary')
        self.clear_button.place(x=344, y=T['height'] - 82)

        self.set_connection_state('disconnected', active=False)

    def set_connection_state(self, state, *, active):
        self.connection_button.configure(text='Desconectar' if active else 'Conectar ESP32')
        messages = {
            'disconnected': 'Activa la Wi-Fi del PC y conecta.',
            'waiting': 'Esperando la conexión del ESP32...',
            'connected': 'Medidas recibidas y guardadas.',
            'unavailable': 'No se pudo conectar. Revisa la terminal.',
        }
        self.status.set_state(state, messages[state])
