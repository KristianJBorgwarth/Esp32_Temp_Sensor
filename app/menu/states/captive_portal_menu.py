from lib.state_machine import IState
import helpers.import_helper as imph

class CaptivePortalMenu(IState):
    def __init__(self):
        super().__init__()
        app = imph.import_app()
        print(len(app._objects))
        self.oled = app.get_object("oled")
        self.captive_portal = app.get_object("cpm")
    
    def enter(self):
        if self.captive_portal is not None:
            self.captive_portal.web_server()
        else:
            print("Captive Portal Manager not found")

    def execute(self):
        self.oled.print_to_screen("Captive Portal")

    def exit(self):
        pass

    