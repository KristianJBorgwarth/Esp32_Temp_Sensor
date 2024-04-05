from lib.state_machine import IState
from app.menu.items.main_menu_items import SettingsMenuItem, TemperatureMenuItem
from app.menu.items.core_menu_items import ExitMenuItem
import helpers.import_helper as imph

class MainMenuState(IState):
    def __init__(self):
        self.oled = imph.import_app().get_object("oled")
        self.input_handler = imph.import_app().get_object("input")
        self.menu_items = None 
        self.selected_item = 0
        
    def enter(self):
        self.menu_items = [SettingsMenuItem(), TemperatureMenuItem(), ExitMenuItem()]

    def execute(self):
        joystick_input_value = self.input_handler.read_joystick_input()
        button_input_value = self.input_handler.read_button_input()

        if button_input_value == "A":
            self.menu_items[self.selected_item].command()

        if joystick_input_value:
            if joystick_input_value == "up":
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif joystick_input_value == "down":
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
        
        self.oled.print_menu(self.menu_items, self.selected_item, "MAIN MENU")

    def exit(self):
        pass