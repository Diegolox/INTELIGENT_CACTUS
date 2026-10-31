# Organizacion de la app

- `CODE/main.py`: arranque de la ventana o del receptor (`--receptor`).
- `CODE/application/`: ventana principal, acciones de botones y estado de las lecturas.
- `CODE/network/`: recepcion TCP, guardado JSON y comunicacion con la app.
- `CODE/ui/`: composicion de la pantalla, componentes, iconos y tema.
- `CODE/paths.py`: rutas de imagenes y medidas, tambien para el ejecutable.
- `recibir.py`: acceso al receptor sin abrir la ventana; no duplica su codigo.

Desde la raiz, `python CODE/main.py`. Conectar inicia la escucha TCP y Desconectar
la detiene. Limpiar solo vacia la pantalla. Las medidas se conservan en `medidas/`.
Los valores simulados pertenecen al ESP32; la app Python muestra lo que recibe.

`crear_exe.bat` compila a `INTELIGENT_CACTUS/`, con temporales fuera de CODE.
Para distribuir la app, copia toda esa carpeta. No se necesita Python instalado.
