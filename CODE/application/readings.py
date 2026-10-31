"""Estado compartido de las cinco lecturas, seguro para varios hilos."""
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



# La app usa esta instancia por defecto. No se crea ninguna ventana al importar.
interface_values = InterfaceValues()


def set_values(**values):
    """Actualiza varias lecturas del estado compartido."""
    interface_values.update(values)


def set_value(sensor, value):
    """Actualiza una sola lectura."""
    interface_values.update({sensor: value})


def clear_values():
    interface_values.clear()
