import socket
import json

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen(1)
    print("Esperando al ESP32 en el puerto 5000...", flush=True)

    while True:
        conexion, direccion = servidor.accept()
        print("ESP32 conectado:", direccion, flush=True)
        try:
            with conexion, conexion.makefile("r", encoding="utf-8") as mensajes:
                for linea in mensajes:
                    try:
                        datos = json.loads(linea)
                        print(datos, flush=True)
                    except json.JSONDecodeError:
                        print("JSON incorrecto:", linea.strip(), flush=True)
        except ConnectionError:
            pass
        print("ESP32 desconectado. Esperando otra conexion...", flush=True)
