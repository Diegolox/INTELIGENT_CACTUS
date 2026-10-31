import socket
import json
from pathlib import Path
from datetime import datetime

# La carpeta se crea junto a este script, aunque lo ejecutes desde otra carpeta.
carpeta = Path(__file__).resolve().parent / "medidas"
carpeta.mkdir(exist_ok=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    # En Windows, reserva el puerto para un solo receptor.
    if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    else:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", 5000))
    servidor.listen(1)
    print("Receptor iniciado en el puerto 5000.", flush=True)
    print("Carpeta de medidas:", carpeta, flush=True)

    while True:
        print("Esperando al ESP32...", flush=True)
        conexion, direccion = servidor.accept()
        print("ESP32 conectado:", direccion[0], flush=True)

        try:
            with conexion, conexion.makefile("r", encoding="utf-8") as mensajes:
                # El ESP32 envia un JSON por linea.
                for linea in mensajes:
                    try:
                        datos = json.loads(linea)
                    except json.JSONDecodeError:
                        print("JSON incorrecto, se ignora:", linea.strip(), flush=True)
                        continue

                    print("Datos recibidos:", json.dumps(datos, ensure_ascii=False), flush=True)

                    # Un archivo por medida. Incluimos microsegundos en el nombre.
                    nombre = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f.json")
                    archivo = carpeta / nombre
                    with archivo.open("x", encoding="utf-8") as fichero:
                        json.dump(datos, fichero, indent=4, ensure_ascii=False)
                    print("Guardado:", archivo.name, flush=True)

        except ConnectionError:
            print("Se ha perdido la conexion.", flush=True)

        print("ESP32 desconectado.", flush=True)
