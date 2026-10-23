"""Carga de iconos externos transparentes, independiente del directorio de ejecución."""
from functools import lru_cache
from pathlib import Path
from PIL import Image
import customtkinter as ctk

ICON_DIRECTORY = Path(__file__).resolve().parents[2] / 'assets' / 'icons'
ICON_NAMES = {'temperature', 'humidity', 'light'}

@lru_cache(maxsize=3)
def _load_image(name):
    if name not in ICON_NAMES:
        raise ValueError(f'Icono desconocido: {name}')
    with Image.open(ICON_DIRECTORY / f'{name}.png') as source:
        return source.convert('RGBA')

def sensor_icon(name, size):
    image = _load_image(name)
    return ctk.CTkImage(light_image=image, dark_image=image, size=(size, size))
