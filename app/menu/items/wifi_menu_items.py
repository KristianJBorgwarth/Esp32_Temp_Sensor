from app.menu.items.core_menu_items import MenuItem

class CaptivePortalMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "PORTAL"

    def command(self):
        pass

class SaveWifiMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "SAVED WIFI"

    def command(self):
        pass