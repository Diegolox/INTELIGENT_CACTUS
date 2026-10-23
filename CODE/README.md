# Inteligent Cactus · interfaz

Desde la raíz del repositorio:

```sh
python -m pip install -r CODE/requirements.txt
python CODE/main.py
```

## Cambiar valores desde otro fichero

`interface_values.py` separa las lecturas de la pantalla. Edita su diccionario `INITIAL_VALUES` y reinicia la app para cambiar los valores de arranque. `None` muestra una raya. Los valores de Demo también se editan en ese fichero, en `DEMO_VALUES`.

Para actualizar lecturas mientras la app está abierta, desde otro módulo del **mismo programa**:

```python
from interface_values import set_values, set_value, clear_values

set_values(air_temperature=25.2, air_humidity=43)
set_value('light', 9800)
# clear_values()  # Borra todas las lecturas.
```

Cada actualización conserva las lecturas que no se incluyen. Se pueden llamar estas funciones desde un hilo del receptor: la app recoge los cambios cada 150 ms y actualiza la pantalla en su propio hilo. Cero es un valor válido, None limpia una lectura. Una clave desconocida, un booleano o un valor no finito produce ValueError sin aplicar ningún cambio.

| Clave | Lectura | Unidad |
| --- | --- | --- |
| `air_temperature` | Temp. Amb. | °C |
| `air_humidity` | Hum. Amb. | % |
| `soil_temperature` | Temp. Sus. | °C |
| `soil_moisture` | Hum. Sus. | % |
| `light` | Luz | lx |

Ejemplo completo editable y ejecutable:

```sh
python CODE/example_values.py
```

Los cambios en memoria no se guardan al cerrar la app. Ejecutar un segundo proceso Python independiente no comparte estos valores; para eso se necesitaría comunicación entre procesos. Editar INITIAL_VALUES con la app abierta requiere reiniciarla.

`app.submit_readings(diccionario)` sigue disponible. Mantiene su comportamiento de paquete completo: los campos ausentes se limpian. Opcionalmente se puede pasar una instancia independiente de `InterfaceValues` al constructor `App(values=...)`.

## Cambiar las funciones de los botones

Edita `button_actions.py`. `on_demo(app)` y `on_clear(app)` son las funciones de ejemplo; puedes sustituir su contenido por llamadas a tu propio código. En `BUTTONS` se cambia tanto el texto de cada botón como la función asignada. Usa el nombre de la función sin paréntesis.

```python
def mi_accion(app):
    # Conserva las demás lecturas y actualiza estas dos.
    app.values.update({'air_temperature': 26.5, 'light': 9000})

BUTTONS = {
    'demo': {'text': 'Actualizar', 'action': mi_accion},
    'clear': {'text': 'Limpiar', 'action': on_clear},
}
```

Mantén las claves `demo` y `clear`, que corresponden a los dos botones existentes. La función recibe la app abierta y la pantalla se refresca después de ejecutarla. Si tu función no recibe argumentos, llámala desde una función envolvente: `def on_demo(app): mi_funcion()`.

Las acciones se ejecutan en el hilo de la interfaz. Las operaciones de red o cálculos que tarden deben ir en un hilo de trabajo; desde ese hilo se puede actualizar `app.values`, pero no manipular widgets. Para cambiar textos o código fuente, reinicia la app. Una reasignación de `BUTTONS['demo']['action']` desde otro módulo del mismo programa se aplica en la siguiente pulsación.

## Archivos

- `main.py`: inicio habitual.
- `interface_values.py`: valores iniciales, demostración y funciones de actualización.
- `example_values.py`: ejemplo de modificación desde otro fichero.
- `button_actions.py`: textos y acciones editables de los botones.
- `app.py`: coordinación de la ventana, actualización y cierre.
- `ui/layout.py`: elementos y posiciones.
- `ui/components.py`: componentes reutilizables.
- `ui/data_panel.py`: cinco sensores y su presentación.
- `styles/theme.json` y `STYLES.md`: estilos.
- `receiver_monitor.py`: observa los estados del receptor existente.

## Enlace ESP32

Al abrir, la app inicia `network/receiver.py` como proceso independiente y observa sus mensajes de conexión, sin modificar ese archivo. El indicador es amarillo en espera o sin estado verificable, verde cuando acepta el ESP32 y rojo cuando se cierra el enlace TCP. No inspecciona directamente la asociación Wi-Fi. Demo y Limpiar no cambian su estado. La app cierra únicamente el receptor que ella misma inicia.

Esta integración observa la conexión; el mapeo de los mensajes de red a las cinco lecturas queda en el código del receptor. Las nuevas funciones no modifican ese protocolo.
