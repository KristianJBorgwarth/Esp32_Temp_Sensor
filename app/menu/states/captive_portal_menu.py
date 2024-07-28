from lib.state_machine import IState
import helpers.import_helper as imph

class CaptivePortalMenu(IState):
    def __init__(self):
        super().__init__()
        self.app = imph.import_app()
        self.oled = self.app.get_object("oled")
        self.captive_portal = self.app.get_object("cpm")
        self.input_handler = self.app.get_object("input")
    
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
        if button_input == "B":
            self.captive_portal.shutdown_portal()
            self.app.get_object("msm", "update").go_back()
        else:
            self.captive_portal.run_web_server()

    def exit(self):
        super().exit()

    