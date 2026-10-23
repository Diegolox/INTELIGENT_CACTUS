"""Ventana vertical: imagen central grande y valores a ambos lados."""
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageOps
from styles.theme import THEME as T
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
    def __init__(self, root, on_demo, on_clear):
        asset = Path(__file__).resolve().parents[2] / 'assets' / 'cactus-limon-pastel.png'
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
        self.status.place(x=18, y=T['height'] - 34)
        self.panel = DataPanel(root, SENSOR_POSITIONS)
        self.demo_button = AppButton(root, text='Demo', command=on_demo, width=120)
        self.demo_button.place(x=202, y=T['height'] - 82)
        self.clear_button = AppButton(root, text='Limpiar', command=on_clear, width=120, variant='secondary')
        self.clear_button.place(x=338, y=T['height'] - 82)
