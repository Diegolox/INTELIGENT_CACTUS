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

## Botones y estado de conexion

La app arranca desconectada. Activa primero el punto de acceso Wi-Fi del PC.

- **Conectar ESP32** abre el receptor TCP en el puerto 5000. El ESP32 se conecta
  automaticamente cuando detecta que el receptor esta disponible.
- **Desconectar** cierra el receptor y libera el puerto. Se conservan las ultimas
  lecturas y los archivos guardados. Puedes volver a conectar con el mismo boton.
- **Limpiar** borra las lecturas de la pantalla. No desconecta ni borra los JSON;
  la siguiente medida recibida vuelve a aparecer.

El circulo indica el estado real del enlace: rojo desconectado o error, amarillo
esperando al ESP32, verde conectado. Un fallo al abrir el puerto se muestra en la
pantalla y en la terminal; cierra cualquier receptor independiente y reintenta.
Si el ESP32 pierde la conexion, el receptor sigue esperando para reconectarlo.

Los botones se definen en `button_actions.py`, con las claves `connect` y `clear`.
Cada funcion recibe la app abierta; no crees otra ventana dentro de una accion.
La demostracion sigue disponible por codigo con `app.show_demo()` o
`app.values.demo()`, pero ya no ocupa un boton de la pantalla.

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
- `receiver_monitor.py`: inicia el receptor y pasa el estado y las lecturas a la app.

## Enlace ESP32

1. Activa el punto de acceso Wi-Fi del PC y carga el firmware del ESP32.
2. Cierra cualquier receptor que hayas ejecutado por separado.
3. Desde la raiz del proyecto ejecuta `python CODE/main.py`.
4. Pulsa **Conectar ESP32**.

Al pulsar Conectar ESP32, la app inicia `recibir.py`, muestra en la terminal el proceso de
conexion y los datos, y actualiza las cinco lecturas con `App.submit_readings()`.
El indicador muestra el estado del enlace TCP, no la asociacion Wi-Fi.
No ejecutes `recibir.py` a la vez que la app: ambos usan el puerto 5000.

El ESP32 envia un JSON por linea cada dos segundos con las claves `ta`, `ts`,
`ha`, `hs` y `luz`. Los valores actuales son simulados y varian ligeramente.
`receiver_monitor.py` traduce esas claves a `air_temperature`, `soil_temperature`,
`air_humidity`, `soil_moisture` y `light`. Las lecturas se actualizan en el estado
compartido; la propia app refresca la pantalla desde el hilo de la interfaz.

Cada JSON recibido se guarda con fecha y hora en `medidas`, junto a `recibir.py`.
Cerrar la app detiene el receptor que ella inicio y libera el puerto.
`python recibir.py` sigue disponible para recibir y guardar sin abrir la ventana.
`CODE/network/receiver.py` tambien ejecuta ese mismo receptor, sin duplicar codigo.
