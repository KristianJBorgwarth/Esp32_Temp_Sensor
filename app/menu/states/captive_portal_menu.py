from lib.state_machine import IState
import helpers.import_helper as imph

class CaptivePortalMenu(IState):
    def __init__(self):
        super().__init__()
        app = imph.import_app()
        print(len(app._objects))
        self.oled = app.get_object("oled")
        self.captive_portal = app.get_object("cpm")
        self.input_handler = app.get_object("input")
    
    def enter(self):
        if self.captive_portal is None:
            raise Exception("Captive Portal Manager not found")
        self.oled.print_to_screen("SSID:"+self.captive_portal.ap_ssid + "\n" + 
                                "PW:"+self.captive_portal.ap_password + "\n" +
                                "IP:"+self.captive_portal.wlan_ap.ifconfig()[0] + "\n" +
                                "Press B to exit")
        self.captive_portal.setup_web_server()

    def execute(self):
        button_input = self.input_handler.read_button_input()
        self.captive_portal.run_web_server()


    def exit(self):
        pass

    