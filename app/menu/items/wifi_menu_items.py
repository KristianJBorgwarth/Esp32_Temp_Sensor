from app.menu.items.core_menu_items import MenuItem
import helpers.import_helper as imph
from app.menu.states.captive_portal_menu import CaptivePortalMenu

class CaptivePortalMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "PORTAL"

    def command(self):
        imph.import_app().get_object("msm", "update").change_state(CaptivePortalMenu())

class SaveWifiMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "SAVED WIFI"

    def command(self):
        pass