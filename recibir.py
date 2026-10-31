"""Acceso al receptor sin abrir la interfaz."""
from pathlib import Path
import sys

if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent / 'CODE'))
    from network.receiver import recibir
    recibir()
