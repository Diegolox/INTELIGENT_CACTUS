"""Inicio alternativo del mismo receptor que utiliza la app."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    receptor = Path(__file__).resolve().parents[2] / 'recibir.py'
    runpy.run_path(str(receptor), run_name='__main__')
