from app.handlers.oled_handler import OLEDHandler as oled
from lib.state_machine import IState
from app.application import Application

class MainMenuState(IState):
    def __init__(self, oled: oled, app: Application):
        self.oled = oled
        self.app = app
        self.input_handler = app.get_object("input")
        
    def enter(self):
        self.oled.print_to_screen("Main Menu")

    def execute(self):
        input_value = self.input_handler.read_joystick_input()
        print(input_value)
        

    def exit(self):
        pass