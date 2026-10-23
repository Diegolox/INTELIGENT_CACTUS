# Inteligent Cactus · interfaz

Desde la raíz del repositorio:

```sh
python -m pip install -r CODE/requirements.txt
python CODE/main.py
```

Arranca sin datos. «Demo» carga cinco valores simulados. «Limpiar» restaura el estado vacío. No inicia ni importa el receptor y no modifica `network/`.

## Archivos

- `main.py`: inicio.
- `app.py`: coordinación, acciones, cola de lecturas y cierre.
- `ui/layout.py`: elementos y posiciones.
- `ui/components.py`: AppLabel, AppButton, AppEntry, AppTextbox, DataValue.
- `ui/data_panel.py`: definición y presentación de cinco sensores.
- `styles/theme.json`: estilos. `STYLES.md`: guía visual.

## Integración posterior

`app.submit_readings(diccionario)` admite llamadas desde otro hilo. Claves propuestas: `soil_moisture` (%), `air_temperature` (°C), `air_humidity` (%), `light` (lx), `soil_temperature` (°C). Valores numéricos finitos o None; campos ausentes aparecen como raya. No impone un protocolo de red.

La humedad del sustrato necesita calibración. No se deducen consejos de riego de las lecturas. Recibir datos no demuestra que el Wi-Fi siga conectado.

Los lectores usan fondo carbón, borde verde y valores monoespaciados. El icono pixel art está en `assets/cactus.ico` (en la raíz del repositorio).

## Indicador de enlace ESP32

Al abrir la app, `receiver_monitor.py` inicia el receptor existente como un proceso independiente y observa sus mensajes de conexión. No modifica `network/receiver.py`. El círculo inferior es amarillo en espera, verde cuando el receptor acepta el ESP32 y rojo cuando se cierra ese enlace. Un receptor no disponible (por ejemplo, puerto 5000 ocupado por otra ejecución) se indica en amarillo con «Sin estado». La app cierra únicamente el proceso receptor que ella misma inicia.

Este indicador refleja el enlace TCP con el ESP32; no inspecciona la asociación Wi-Fi del ordenador o del dispositivo. Demo y Limpiar no cambian el estado del enlace. Esta integración observa solo la conexión, sin cambiar el formato de los datos ni mapear todavía sus campos a las cinco lecturas.
