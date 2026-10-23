"""Ejemplo: ejecuta python CODE/example_values.py desde la raíz del repositorio."""
from app import App
from interface_values import set_values, set_value


def load_values():
    # Edita estos números para probar otros valores sin modificar app.py.
    set_values(
        air_temperature=25.2,
        air_humidity=43,
        soil_temperature=23.1,
        soil_moisture=17,
        light=9800,
    )
    # También puedes cambiar una sola lectura; las demás se conservan.
    set_value('light', 10500)


if __name__ == '__main__':
    load_values()
    App().mainloop()
