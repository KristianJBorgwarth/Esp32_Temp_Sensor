from lib.state_machine import IState
from app.menu.items.core_menu_items import BackMenuItem
from app.menu.items.wifi_menu_items import CaptivePortalMenuItem, SaveWifiMenuItem

class WifiMenuState(IState):
    def __init__(self):
        super().__init__()
        self.menu_name = "WIFI"
        
    def enter(self):
        self.menu_items = [CaptivePortalMenuItem(), SaveWifiMenuItem(), BackMenuItem()]

    def execute(self):
        super().execute()
        
    def exit(self):
        super().exit()