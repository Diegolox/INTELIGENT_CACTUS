"""Rutas comunes para el codigo fuente y el ejecutable."""
from pathlib import Path
import sys

PROJECT_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_DIR / 'assets'
MEASURES_DIR = PROJECT_DIR / 'medidas'
