import helpers.import_helper as imph
import time 
class MenuItem:
    def __init__(self):
        self.display_text = ""

    def command(self):
        raise NotImplementedError("Subclasses should implement this!")
    
class BackMenuItem(MenuItem):
    def __init__(self):
        self.display_text = "BACK"
    
    def command(self):
        stm = imph.import_app().get_object("msm", "update")
        stm.go_back()
        
class ExitMenuItem(MenuItem):
    def __init__(self):
        self.display_text = "EXIT"
    
    def command(self):
        app = imph.import_app()
        app.delete_object("msm", "update")
        oled = app.get_object("oled")
        for i in range(5):
            oled.print_to_screen("Shutting down:"+str(5 - i))
            time.sleep(1)
        app.stop()
        app.get_object("oled").clear_screen()
        
        
        