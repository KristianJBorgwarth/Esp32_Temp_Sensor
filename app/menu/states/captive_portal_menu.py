from lib.state_machine import IState
import helpers.import_helper as imph

class CaptivePortalMenu(IState):
    def __init__(self):
        super().__init__()
        self.oled = imph.import_app().get_object("oled")
        self.captive_portal = imph.import_app().get_object("cpm")
    
    def enter(self):
        self.captive_portal.start_web_server()

    def execute(self):
        self.oled.print_to_screen("Captive Portal", 0, 0)

    def exit(self):
        pass

    