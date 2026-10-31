# Inteligent Cactus

Aplicación para recibir por Wi-Fi las medidas de un ESP32, mostrarlas en pantalla y guardarlas en archivos JSON.

<img src="assets/captura-app.png" alt="Aplicación Inteligent Cactus con medidas simuladas" width="420">

**Actualmente las medidas son simuladas** y cambian ligeramente cada dos segundos.

## Funcionamiento

1. El PC crea una red Wi-Fi mediante su punto de acceso.
2. El ESP32 se conecta a esa red.
3. En la app, **Conectar ESP32** inicia el receptor TCP en el puerto `5000`.
4. El ESP32 envía las cinco medidas en un JSON:

```json
{"ta":24.3,"ts":21.8,"ha":60.5,"hs":35.2,"luz":123456}
```

`ta` y `ts`: temperatura ambiente y del suelo (°C).
`ha` y `hs`: humedad ambiente y del suelo (%).
`luz`: iluminación simulada (lx).

Cada medida se guarda en `medidas/` con fecha y hora. El círculo indica: amarillo en espera, verde conectado y rojo desconectado o error.

## Ejecutar

- Cargar `ESP32_INTELIGENT_CACTUS` con PlatformIO, configurando Wi-Fi, contraseña e IP del PC en `src/main.cpp`.
- Activar el punto de acceso Wi-Fi del PC.
- Desde la carpeta del proyecto:

```sh
python -m pip install -r CODE/requirements.txt
python CODE/main.py
```

Pulsar **Conectar ESP32**. **Desconectar** cierra el receptor; **Limpiar** borra solo las lecturas de la pantalla.

## Código principal

- **ESP32 — `main.cpp`:** `initWifi()` conecta a la red, `generarMedida()` crea los valores y `enviarMedida()` envía el JSON. `delay(2000)` separa los envíos dos segundos.
- **PC — `recibir.py`:** lee un JSON por línea; `json.loads()` interpreta los datos y `json.dump()` los guarda.
- **App — `CODE/`:** `receiver_monitor.py` pasa las medidas a `submit_readings()`, y la interfaz actualiza las cinco lecturas.

Para usar sensores reales, se sustituye el contenido de `generarMedida()` por sus lecturas.
