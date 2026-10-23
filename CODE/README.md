# INTELIGENT_CACTUS — aplicación

Aplicación de escritorio en Python con CustomTkinter para recibir datos por Wi-Fi y mostrar sus últimos valores en una interfaz.

## Estado actual

Este proyecto contiene únicamente la estructura inicial. Todos los archivos de código, configuración y dependencias están vacíos. Todavía no se puede ejecutar la aplicación. Este documento describe las responsabilidades previstas y se actualizará cuando acordemos cambios.

## Estructura

```text
CODE/
├── main.py
├── app.py
├── network/
│   └── receiver.py
├── ui/
│   ├── components.py
│   └── data_panel.py
├── styles/
│   ├── theme.json
│   └── theme.py
├── requirements.txt
└── README.md
```

## Función de cada elemento

| Elemento | Responsabilidad prevista |
| --- | --- |
| `main.py` | Punto de entrada: crear la aplicación e iniciar el bucle de la interfaz. |
| `app.py` | Contener la clase `App`, configurar la ventana principal y coordinar el receptor y el panel de datos. Gestionar el inicio y la parada de la recepción y el cierre de la aplicación. |
| `network/` | Agrupar la comunicación de red, separada de la interfaz. |
| `network/receiver.py` | Recibir y validar mensajes del dispositivo en segundo plano y entregar los datos mediante una cola. El protocolo y el formato de los mensajes están pendientes de definir. |
| `ui/` | Agrupar los componentes visuales y el panel de datos. |
| `ui/components.py` | Definir clases reutilizables basadas en CustomTkinter para botones, campos de entrada, cajas de texto y lecturas. Nombres previstos: `AppButton`, `AppEntry`, `AppTextbox` y `DataValue`. Todas tomarán sus estilos del tema central. |
| `ui/data_panel.py` | Contener la clase `DataPanel`, que agrupa las lecturas y actualiza sus nombres, valores y unidades. Mostrar también el estado de recepción y la hora del último mensaje cuando se implemente la pantalla. |
| `styles/` | Centralizar el aspecto visual de la aplicación. |
| `styles/theme.json` | Almacenar colores, fuentes, tamaños y bordes. Usar nombres según su función, como `background`, `surface`, `primary`, `text` y `error`, para cambiar la paleta desde un solo archivo. Está vacío por ahora; habrá que añadir JSON válido antes de cargarlo. |
| `styles/theme.py` | Cargar y validar el tema y facilitar su uso desde los componentes. |
| `requirements.txt` | Enumerar las dependencias necesarias para ejecutar la aplicación. Se completará al implementar el proyecto. |
| `README.md` | Documentar la estructura, las decisiones acordadas y, cuando existan, las instrucciones de instalación y uso. |

## Flujo previsto

```text
Dispositivo → conexión Wi-Fi → receptor → cola de datos → interfaz
```

El receptor trabajará en segundo plano. La interfaz consultará la cola desde su propio bucle y actualizará los componentes sin bloquear la ventana. El receptor no modificará directamente los elementos visuales.

## Criterios acordados

- Usar CustomTkinter para la interfaz.
- Crear clases propias para los componentes reutilizables.
- Centralizar los estilos; evitar colores definidos directamente en las pantallas.
- Mostrar los últimos datos recibidos y mantenerlos en memoria.
- Mantener un alcance sencillo: recepción y visualización, sin base de datos ni historial por ahora.
- Definir el protocolo de red, el formato de los mensajes y los campos que se mostrarán antes de implementar la recepción.
- Actualizar este documento cuando acordemos cambios en la estructura o el comportamiento.

