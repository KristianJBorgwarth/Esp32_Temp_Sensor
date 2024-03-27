from app.handlers.oled_handler import OLEDHandler as oled
from lib.state_machine import IState
from app.menu.items.settings_items import WifiMenuItem, UpdateMenuItem
from app.menu.items.core_menu_items import BackMenuItem

class SettingsMenuState(IState):
    def __init__(self, oled: oled):
        self.oled = oled
        from app.application import Application 
        self.app = Application()
        self.input_handler = self.app.get_object("input")
        self.menu_items = None
        self.selected_item = 0
        
    def enter(self):
        self.menu_items = [WifiMenuItem(), UpdateMenuItem(), BackMenuItem()]

    def execute(self):
        input_value = self.input_handler.read_joystick_input()
        b_input_value = self.input_handler.read_button_input()
        
        if b_input_value == "A":
            self.menu_items[self.selected_item].command()

        if input_value:
            if input_value == "up":
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif input_value == "down":
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
        
        self.oled.print_menu(self.menu_items, self.selected_item, "Settings Menu")

    def exit(self):
        pass