# ESP32 → PC: tres sensores en JSON

Proyecto minimo e independiente. El proyecto anterior y sus archivos extra siguen intactos.

1. Abre esta carpeta `ESP32` con PlatformIO.
2. En `src/main.cpp`, cambia `WIFI_SSID`, `WIFI_PASSWORD` y `PC_IP`.
   Para conocer la IP del PC, ejecuta `ipconfig` en Windows y busca la direccion IPv4 de tu conexion Wi-Fi.
3. Conecta el PC y el ESP32 a la misma red, sin aislamiento entre dispositivos.
4. Abre una terminal en esta carpeta y ejecuta `python recibir.py`.
   Si Windows pregunta, permite a Python acceder a la red privada.
5. Carga el programa al ESP32 con PlatformIO. La dependencia ArduinoJson se instala al compilar.

Cada segundo veras algo como:

```text
{'sensor1': 1200, 'sensor2': 2300, 'sensor3': 800}
```

El ESP32 envia `{"sensor1":1200,"sensor2":2300,"sensor3":800}` seguido de un salto de linea.
El PC lee una linea completa y `json.loads()` la convierte a un diccionario de Python.
El salto de linea separa los mensajes porque TCP puede entregar un mensaje en varias partes o juntar varios.

Python solo usa `socket` y `json`, incluidos en Python: no necesitas instalar paquetes.
El PC escucha y el ESP32 se conecta. Si se desconecta, vuelve a intentar conectar.
Para parar el receptor, pulsa Ctrl+C.

Las tres lecturas son ejemplos analogicos en GPIO 32, 33 y 34 (ADC1).
Sin sensores conectados los valores fluctuan. No representan temperatura ni porcentajes.
Usa sensores con salida compatible con 3,3 V y masa comun; no conectes 5 V a los GPIO.
Cuando se definan los sensores reales, basta con sustituir las tres asignaciones en `main.cpp`.
