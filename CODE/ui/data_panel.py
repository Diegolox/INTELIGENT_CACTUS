import customtkinter as ctk
from styles.theme import THEME as T
from ui.components import AppLabel,DataValue
SENSORS=(
('soil_moisture','Humedad del sustrato','%','Agua presente en la tierra'),
('air_temperature','Temperatura ambiente','°C','Temperatura alrededor del cactus'),
('air_humidity','Humedad ambiental','%','Humedad relativa del aire'),
('light','Luz ambiental','lx','Iluminación que recibe la planta'),
('soil_temperature','Temperatura del sustrato','°C','Temperatura en la zona de raíces'))
class DataPanel:
    """Controla las cajas distribuidas alrededor del cactus."""
    def __init__(self, master, positions):
        from ui.components import SensorBox
        self.readings = {}
        for key, name, unit, description in SENSORS:
            x, y, context = positions[key]
            titles = {
                'air_temperature': 'Temp. Amb.',
                'air_humidity': 'Hum. Amb.',
                'soil_temperature': 'Temp. Sus.',
                'soil_moisture': 'Hum. Sus.',
                'light': 'Luz',
            }
            kind = 'light' if key == 'light' else ('humidity' if 'humidity' in key or 'moisture' in key else 'temperature')
            item = SensorBox(master, titles[key], unit, context, kind=kind)
            item.place(x=x, y=y)
            self.readings[key] = item
        self.updated = AppLabel(master, '', size=12, muted=True)
        self.updated.place(relx=0.5, y=T['height'] - 34, anchor='n')

    def update_values(self, values, timestamp):
        for key, item in self.readings.items():
            item.set_value(values.get(key))
        self.updated.configure(text=f'Actualizado {timestamp}')
