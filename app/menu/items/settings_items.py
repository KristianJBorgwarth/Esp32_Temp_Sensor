from app.menu.items.core_menu_items import MenuItem

class WifiMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "Wifi"
    
    def command(self):
        print("Wifi menu item selected")

class UpdateMenuItem(MenuItem):
    def __init__(self):
        super().__init__()
        self.display_text = "Update"
    
    def command(self):
        print("Update menu item selected")
        