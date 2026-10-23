"""Valores de la interfaz, editables sin depender de CustomTkinter.

Edita INITIAL_VALUES para cambiar el arranque. Desde otro fichero del mismo
programa importa set_values o set_value para actualizar las lecturas en vivo.
None muestra una raya. No modifica la conexión ni el receptor.
"""
from datetime import datetime
import math
from threading import Lock

# Cambia estos valores para configurar las lecturas al abrir la app.
INITIAL_VALUES = {
    'air_temperature': None,   # Temp. Amb. · °C
    'air_humidity': None,      # Hum. Amb.  · %
    'soil_temperature': None,  # Temp. Sus. · °C
    'soil_moisture': None,     # Hum. Sus.  · %
    'light': None,             # Luz        · lx
}

DEMO_VALUES = {
    'air_temperature': 24.6,
    'air_humidity': 42,
    'soil_temperature': 22.8,
    'soil_moisture': 18,
    'light': 12500,
}


class InterfaceValues:
    """Estado compartido seguro para la interfaz y los hilos del receptor."""
    def __init__(self, initial=None):
        self._lock = Lock()
        self._values = dict.fromkeys(INITIAL_VALUES)
        self._values.update(self._validate(INITIAL_VALUES if initial is None else initial))
        self._version = 0
        self._source = 'initial'
        self._timestamp = None

    @staticmethod
    def _validate(changes):
        changes = dict(changes)
        unknown = changes.keys() - INITIAL_VALUES.keys()
        if unknown:
            raise ValueError(f'Sensores desconocidos: {", ".join(sorted(unknown))}')
        for key, value in changes.items():
            if value is not None and (isinstance(value, bool) or
                    not isinstance(value, (int, float)) or not math.isfinite(value)):
                raise ValueError(f'Lectura inválida: {key}')
        return changes

    def update(self, changes, *, replace=False, source='live'):
        """Actualización parcial por defecto; validación completa antes de guardar."""
        clean = self._validate(changes)
        with self._lock:
            if replace:
                self._values = dict.fromkeys(INITIAL_VALUES)
            self._values.update(clean)
            self._version += 1
            self._source = source
            self._timestamp = datetime.now()

    def snapshot(self):
        """Devuelve una copia; el llamante no puede alterar el estado interno."""
        with self._lock:
            return self._version, self._values.copy(), self._source, self._timestamp

    def clear(self):
        self.update({}, replace=True, source='clear')

    def demo(self):
        self.update(DEMO_VALUES, replace=True, source='demo')


# La app usa esta instancia por defecto. No se crea ninguna ventana al importar.
interface_values = InterfaceValues()


def set_values(**values):
    """Ejemplo: set_values(air_temperature=25.2, air_humidity=43)."""
    interface_values.update(values)


def set_value(sensor, value):
    """Ejemplo: set_value('light', 9800)."""
    interface_values.update({sensor: value})


def clear_values():
    interface_values.clear()
