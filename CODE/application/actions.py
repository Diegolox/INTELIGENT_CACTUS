"""Textos y funciones de los dos botones de la app."""


def on_connect(app):
    """Inicia o detiene el receptor del ESP32."""
    app.toggle_connection()


def on_clear(app):
    """Borra las lecturas de la pantalla, sin cerrar la conexion ni borrar archivos."""
    app.values.clear()


BUTTONS = {
    'connect': {'text': 'Conectar ESP32', 'action': on_connect},
    'clear': {'text': 'Limpiar', 'action': on_clear},
}


def execute(button_id, app):
    action = BUTTONS[button_id]['action']
    if not callable(action):
        raise TypeError(f'La acción de {button_id} debe ser una función, sin paréntesis.')
    return action(app)
