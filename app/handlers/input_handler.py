from machine import ADC, Pin

class InputHandler:
    def __init__(self):
        self.a_button = Pin(26, Pin.IN, Pin.PULL_UP)
        self.b_button = Pin(5, Pin.IN, Pin.PULL_UP)
        self.joy_stick = ADC(Pin(36))
        self.joy_stick.atten(ADC.ATTN_11DB)
        self.can_click = True
        
    def read_button_input(self):
        if self.a_button.value() == 0:
            return "A"
        if self.b_button.value() == 0:
            return "B"
    
    def read_joystick_input(self):
        val_in = self.joy_stick.read()
        direction = ""
        if val_in < 10 and self.can_click:
            direction = "down"
            self.can_click = False
        elif val_in > 1000 and val_in < 2000 and self.can_click:
            direction = "up"
            self.can_click = False
        if val_in > 4000 and self.can_click == False:
            self.can_click = True
        return direction        
            