import helpers.import_helper as imph
from app.menu.states.settings_menu import SettingsMenuState
from app.menu.items.core_menu_items import MenuItem
from app.menu.states.temperature_menu import TemperatureMenuState

class SettingsMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "SETTINGS"
    
    def command(self):
        app = imph.import_app()
        stm = app.get_object("msm", "update")
        stm.change_state(SettingsMenuState())

class TemperatureMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "TEMPERATURE"
    
    def command(self):
        app = imph.import_app()
        stm = app.get_object("msm", "update")
        stm.change_state(TemperatureMenuState())
        