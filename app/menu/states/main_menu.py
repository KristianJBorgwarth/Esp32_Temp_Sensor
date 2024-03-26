from app.handlers.oled_handler import OLEDHandler as oled
from lib.state_machine import IState

class MainMenuState(IState):
    def __init__(self, oled: oled):
        self.oled = oled
        from app.application import Application 
        self.app = Application()
        self.input_handler = self.app.get_object("input")
        self.menu_items = [WifiMenuItem(), ExitMenuItem()]
        self.selected_item = 0
        
    def enter(self):
        pass

    def execute(self):
        input_value = self.input_handler.read_joystick_input()
        if input_value:
            if input_value == "up":
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif input_value == "down":
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif input_value == "press":
                self.menu_items[self.selected_item].command()
        
        self.oled.print_menu(self.menu_items, self.selected_item, "Main Menu")

    def exit(self):
        pass


class WifiMenuItem:
    def __init__(self):
        self.display_text = "Settings"
    
    def command(self):
        print("Wifi menu item selected")

class ExitMenuItem:
    def __init__(self):
        self.display_text = "Exit"
    
    def command(self):
        print("Exit menu item selected")