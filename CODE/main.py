"""Entrada unica de la app y de su receptor en segundo plano."""
import sys

if __name__ == '__main__':
    if '--receptor' in sys.argv:
        from network.receiver import recibir
        recibir()
    else:
        from application.app import App
        App().mainloop()
