from lib.state_machine import IState
from app.menu.items.main_menu_items import SettingsMenuItem, TemperatureMenuItem
from app.menu.items.core_menu_items import ExitMenuItem

class MainMenuState(IState):
    def __init__(self):
        super().__init__()
        self.menu_name = "MAIN MENU"
        
    def enter(self):
        self.menu_items = [SettingsMenuItem(), TemperatureMenuItem(), ExitMenuItem()]

    def execute(self):
        super().execute()

    def exit(self):
        super().exit()