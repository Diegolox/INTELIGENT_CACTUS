# Estilos de la interfaz

Fuente de verdad: `styles/theme.json`. Composición: `ui/layout.py`.

- Ventana vertical fija de 660 × 700 unidades lógicas. Renderizado DPI nativo de Windows para evitar ampliación borrosa; escala única para imagen y controles. El tamaño físico se adapta a la escala de pantalla.
- Imagen original intacta, adaptada al encuadre solo en memoria.
- Cinco lectores horizontales de 174 × 62, fondo salvia claro, borde verde medio de 2 píxeles y esquinas de radio 12.
- Etiqueta en Segoe UI negrita, valor en Consolas alineado a la derecha. Unidades entre corchetes junto al nombre.
- Iconos de línea externos para temperatura, humedad y luz, sin conectores hacia la planta. Originales SVG y copias PNG RGBA en `assets/icons/`. Importados con `ui/icons.py`, sin dibujo sobre Canvas.
- Orden en cada lector: etiqueta con unidad, icono de 24 píxeles y valor alineado a la derecha. Fondo salvia claro #E1EBCF y borde verde #6D8B5E; colores independientes en el tema.
- Los PNG transparentes se entregan a 96 × 96 para mantener nitidez al mostrarse pequeños. No se necesita una librería SVG para ejecutar la app.
- T. aire y H. aire corresponden al ambiente; T. suelo y H. suelo, al sustrato. Luz en lux.
- Cabecera «Mi cactus», estado breve y acciones «Demo» / «Limpiar». Hora de actualización solo después de recibir datos.
- Icono de aplicación pixel art: `assets/cactus.ico`, con varios tamaños para Windows.

Etiquetas de 13 y números monoespaciados de 15. Iconos PNG a 96 × 96 con trazo verde oscuro. Cajas alejadas de la silueta: margen exterior de 8, izquierda termina en x=182 y derecha comienza en x=478; la lectura de suelo derecha se sitúa bajo el borde ancho de la maceta.

## Ajuste de color y orden

Interior verde mantequilla pastel #EEF0D6, cálido y desaturado. Cada fila sigue el orden icono → nombre con dos puntos → valor → unidad (por ejemplo, gota Humedad: 42 %). Aire/suelo se identifica con una nota breve sobre el nombre. Las unidades aparecen al final, sin corchetes.

Nombres compactos en una sola fila: Temp. Amb., Hum. Amb., Temp. Sus., Hum. Sus. y Luz. Amb. identifica ambiente y Sus. identifica sustrato. Sin etiquetas de contexto repetidas.

## Controles unificados

Cabecera y lecturas comparten AppPanel. Botones, entradas y cajas multilínea usan el mismo fondo #EEF0D6, borde #6D8B5E de 2 y radio 12. Los botones se iluminan en #DFE7C3 al pasar el cursor. Segoe UI en negrita para títulos y acciones, texto secundario verde apagado, Consolas para valores. Cabecera compacta sobre la zona libre de la fotografía.

## Cabecera e indicador

Título sin contenedor: «Inteligent CACTUS». Indicador discreto abajo a la izquierda, círculo antes del texto: amarillo en espera o sin estado verificable, verde conectado y rojo tras desconexión. Botones de silueta ovalada, sin borde: acción principal verde medio y secundaria verde pastel algo más intenso. Mantienen tipografía y gama de color; se diferencian de los lectores rectangulares con borde.
