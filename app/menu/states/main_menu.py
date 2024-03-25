from app.handlers.oled_handler import OLEDHandler as oled
from lib.state_machine import StateMachine, IState

class MainMenuState(IState):
    def __init__(self, oled: oled):
        self.oled = oled
        
    def enter(self):
        oled.clear()
        oled.display_text("Main Menu", 0, 0)

    def execute(self):
        pass

    def exit(self):
        pass