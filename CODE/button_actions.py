"""Edita aquí los textos y las funciones de los dos botones.

Cada función recibe app, la aplicación abierta. Puedes llamar a tus funciones,
actualizar app.values o consultar sus lecturas. No crees otra App dentro de una
acción. La pantalla se refresca automáticamente al terminar la función.
"""


def on_demo(app):
    """Ejemplo: cargar los valores de demostración de interface_values.py."""
    app.values.demo()


def on_clear(app):
    """Ejemplo: vaciar las cinco lecturas."""
    app.values.clear()


# Mantén las claves demo y clear: identifican los dos lugares de la pantalla.
# Puedes cambiar libremente el texto y la función asignada, sin paréntesis.
BUTTONS = {
    'demo': {
        'text': 'Demo',
        'action': on_demo,
    },
    'clear': {
        'text': 'Limpiar',
        'action': on_clear,
    },
}


def execute(button_id, app):
    """Busca la acción al pulsar, para permitir reasignarla también en ejecución."""
    action = BUTTONS[button_id]['action']
    if not callable(action):
        raise TypeError(f'La acción de {button_id} debe ser una función, sin paréntesis.')
    return action(app)
