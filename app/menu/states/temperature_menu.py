from app.menu.items.core_menu_items import BackMenuItem
from lib.state_machine import IState
from app.menu.items.temp_menu_items import StartMenuItem, StopMenuItem

class TemperatureMenuState(IState):
    def __init__(self):
        super().__init__()
        self.menu_name = "TEMPERATURE"

    def enter(self):
        self.menu_items = [StartMenuItem(), StopMenuItem(), BackMenuItem()]

    def execute(self):
        super().execute()

    def exit(self):
        super().exit()
