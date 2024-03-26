from machine import ADC, Pin
from app.application import Application

class InputHandler:
    def __init__(self, app: Application):
        self.app = app
        self.a_button = Pin(26, Pin.IN, Pin.PULL_UP)
        self.b_button = Pin(5, Pin.IN, Pin.PULL_UP)
        self.joy_stick = ADC(Pin(36))
        self.joy_stick.atten(ADC.ATTN_11DB)
        
    def read_button_input(self):
        if self.a_button.value() == 0:
            print("A button pressed")
        if self.b_button.value() == 0:
            print("B button pressed")
    
    def read_joystick_input(self):
        val_in = self.joy_stick.read()
        direction = ""
        if val_in < 10:
            direction = "down"
        elif val_in > 1000 and val_in < 2000:
            direction = "up"
        return direction        
            