from lib.state_machine import IState
import helpers.import_helper as imph
from app.menu.items.core_menu_items import BackMenuItem
from app.menu.items.wifi_menu_items import CaptivePortalMenuItem, SaveWifiMenuItem

class WifiMenuState(IState):
    def __init__(self, oled):
        super().__init__()
        self.input_handler = imph.import_app().get_object("input")
        self.menu_items = None
        self.selected_item = 0
        self.oled = oled
        

    def enter(self):
        self.menu_items = [CaptivePortalMenuItem(), SaveWifiMenuItem(), BackMenuItem()]

    def execute(self):
        joystick_input_value = self.input_handler.read_joystick_input()
        button_input_value = self.input_handler.read_button_input()

        if button_input_value == "A":
            self.menu_items[self.selected_item].command()
            return

        if joystick_input_value:
            if joystick_input_value == "up":
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif joystick_input_value == "down":
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)

        self.oled.print_menu(self.menu_items, self.selected_item, "WIFI")

    def exit(self):
        print("Exiting wifi menu state")
        self.oled.clear_screen()