from lib.state_machine import IState
from app.menu.items.settings_menu_items import WifiMenuItem, UpdateMenuItem
from app.menu.items.core_menu_items import BackMenuItem

class SettingsMenuState(IState):
    def __init__(self):
        super().__init__()
        self.menu_name = "SETTINGS"
        
    def enter(self):
        self.menu_items = [WifiMenuItem(), UpdateMenuItem(), BackMenuItem()]

    def execute(self):
        super().execute()

    def exit(self):
        super().exit()