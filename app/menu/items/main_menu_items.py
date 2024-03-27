import helpers.import_helper as imph
from app.menu.states.settings_menu import SettingsMenuState as sms
from app.menu.items.core_menu_items import MenuItem

class SettingsMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "Settings"
    
    def command(self):
        app = imph.import_app()
        stm = app.get_object("msm", "update")
        oled = app.get_object("oled")
        stm.change_state(sms(oled))

class TemperatureMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "Temperature"
    
    def command(self):
        pass