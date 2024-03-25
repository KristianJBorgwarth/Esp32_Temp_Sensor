from app.handlers.oled_handler import OLEDHandler as oled
from lib.state_machine import IState
from app.application import Application

class MainMenuState(IState):
    def __init__(self, oled: oled, app: Application):
        self.oled = oled
        self.app = app
        
    def enter(self):
        self.oled.print_to_screen("Main Menu")

    def execute(self):
        print("Main Menu State is running")

    def exit(self):
        pass