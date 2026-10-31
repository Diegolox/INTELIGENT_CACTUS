"""Entrada de la app y del receptor cuando se distribuye como ejecutable."""
import sys
from pathlib import Path
import runpy

if __name__ == '__main__':
    if '--receptor' in sys.argv:
        carpeta = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent.parent
        runpy.run_path(str(carpeta / 'recibir.py'), run_name='__main__')
    else:
        from app import App
        App().mainloop()
