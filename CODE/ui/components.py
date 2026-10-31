import customtkinter as ctk
from ui.theme import THEME as T, font
class AppLabel(ctk.CTkLabel):
    def __init__(self,master,text='',size=14,muted=False,weight='normal',**kw):
        super().__init__(master,text=text,font=font(size,weight),text_color=T['muted' if muted else 'text'],**kw)
class AppPanel(ctk.CTkFrame):
    """Superficie común para cabecera, lecturas y futuros paneles."""
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=T['sensor_background'],
                         border_color=T['sensor_border'], border_width=T['sensor_border_width'],
                         corner_radius=T['sensor_radius'], **kwargs)

class AppButton(ctk.CTkButton):
    def __init__(self, master, variant='primary', **kwargs):
        secondary = variant == 'secondary'
        super().__init__(master, font=font(T['control_font_size'], 'bold'),
                         height=38, corner_radius=19,
                         fg_color=T['button_secondary'] if secondary else T['button_fill'],
                         hover_color=T['button_secondary_hover'] if secondary else T['button_hover'],
                         text_color=T['sensor_text'] if secondary else T['button_text'],
                         border_width=0, **kwargs)

class ConnectionIndicator(ctk.CTkFrame):
    """Estado del enlace ESP32, independiente de los datos de demostración."""
    STATES = {
        'waiting': ('Esperando ESP32', 'status_waiting'),
        'connected': ('Conectado', 'status_connected'),
        'disconnected': ('Desconectado', 'status_disconnected'),
        'unavailable': ('Error de conexión', 'status_disconnected'),
    }

    def __init__(self, master):
        super().__init__(master, height=24, fg_color='transparent')
        self.dot = ctk.CTkFrame(self, width=9, height=9, corner_radius=5,
                               fg_color=T['status_waiting'])
        self.dot.pack(side='left', padx=(0, 8))
        self.label = AppLabel(self, '', size=11, muted=True, height=24)
        self.label.pack(side='left')
        self.set_state('disconnected')

    def set_state(self, state, message=None):
        text, color = self.STATES[state]
        self.state = state
        self.dot.configure(fg_color=T[color])
        self.label.configure(text=text if message is None else message)

class SensorBox(AppPanel):
    """Lectura horizontal de solo lectura, inspirada en un instrumento."""
    def __init__(self, master, name, unit, context, kind='temperature', width=None):
        super().__init__(master, width=width or T['sensor_width'], height=T['sensor_height'])
        self.unit = unit
        self.grid_propagate(False)
        from ui.icons import sensor_icon
        self.icon_image = sensor_icon(kind, T['sensor_icon_size'])
        self.symbol = ctk.CTkLabel(self, text='', image=self.icon_image,
                                  width=T['sensor_icon_size'], height=T['sensor_icon_size'])
        self.symbol.place(x=8, y=19)
        self.name = ctk.CTkLabel(self, text=name if name.endswith('.') else f'{name}:',
                                font=(T['sensor_font'], T['sensor_label_size'], 'bold'),
                                text_color=T['sensor_text'], width=42 if kind == 'light' else 76,
                                height=28, anchor='w')
        self.name.place(x=36, y=17)
        self.value = ctk.CTkLabel(self, text='—', font=(T['value_font'], T['sensor_value_size']),
                                 text_color=T['sensor_value'], width=72 if kind == 'light' else 37,
                                 height=28, anchor='e')
        self.value.place(x=78 if kind == 'light' else 115, y=17)
        self.unit_label = ctk.CTkLabel(self, text=unit, font=(T['sensor_font'], 12),
                                      text_color=T['sensor_text'], width=16, height=28, anchor='w')
        self.unit_label.place(x=154, y=17)

    def set_value(self, value):
        self.value.configure(text='—' if value is None else f'{value:g}')
