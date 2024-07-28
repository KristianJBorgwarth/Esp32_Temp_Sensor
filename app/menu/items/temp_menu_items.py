import helpers.import_helper as imph
from app.menu.items.core_menu_items import MenuItem

class StartMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "START"
        
    def command(self):
        temp_handler = imph.import_app().get_object("temp_sensor")
        temp_handler.start()
        print("Temperature measurement started")

class StopMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "STOP"

    def command(self):
        temp_handler = imph.import_app().get_object("temp_sensor")
        temp_handler.stop()
        print("Temperature measurement stopped")