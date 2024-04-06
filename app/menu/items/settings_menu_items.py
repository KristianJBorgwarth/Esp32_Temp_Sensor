from app.menu.items.core_menu_items import MenuItem
import helpers.import_helper as imph
from app.menu.states.wifi_menu import WifiMenuState
import lib.ugit as ota

class WifiMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "WIFI"
        
    def command(self):
        app = imph.import_app()
        stm = app.get_object("msm", "update")
        oled = app.get_object("oled")
        stm.change_state(WifiMenuState())        

class UpdateMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "UPDATE"
    
    def command(self):
        app = imph.import_app()
        #remove all objects from the app, bc we are going to update the firmware and we have zero fucking memory on this thing
        app.clear_all_objects()
        ota.pull_all(isconnected=True)
        