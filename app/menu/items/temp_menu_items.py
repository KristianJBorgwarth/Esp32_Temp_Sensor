import helpers.import_helper as imph
from app.menu.items.core_menu_items import MenuItem

class StartMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "START"

    def command(self):
        pass

class StopMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "STOP"

    def command(self):
        pass