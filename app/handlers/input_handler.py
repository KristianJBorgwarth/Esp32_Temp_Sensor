from machine import ADC, Pin

class InputHandler:
    JOYSTICK_UP_THRESHOLD = 1000
    JOYSTICK_DOWN_THRESHOLD = 10
    JOYSTICK_RELEASE_THRESHOLD = 4000

    def __init__(self):
        self.a_button = Pin(26, Pin.IN, Pin.PULL_UP)
        self.b_button = Pin(5, Pin.IN, Pin.PULL_UP)
        self.joy_stick = ADC(Pin(36))
        self.joy_stick.atten(ADC.ATTN_11DB)
        self.can_click = True
        self.can_click_a = True
        self.can_click_b = True
        
    def read_button_input(self):
        a_pressed = self.a_button.value() == 0
        b_pressed = self.b_button.value() == 0

         # Process the A button press
        if a_pressed and self.can_click_a:
            self.can_click_a = False  
            return "A"
        if not a_pressed:
            self.can_click_a = True  

        # Process the B button press
        if b_pressed and self.can_click_b:
            self.can_click_b = False  
            return "B"
        if not b_pressed:
            self.can_click_b = True

        return None  

    def read_joystick_input(self):
        val_in = self.joy_stick.read()
        direction = ""
        if val_in < self.JOYSTICK_DOWN_THRESHOLD and self.can_click:
            direction = "down"
            self.can_click = False
        elif val_in > self.JOYSTICK_DOWN_THRESHOLD and val_in < 2000 and self.can_click:
            direction = "up"
            self.can_click = False
        if val_in > self.JOYSTICK_RELEASE_THRESHOLD and self.can_click == False:
            self.can_click = True
        return direction        
            