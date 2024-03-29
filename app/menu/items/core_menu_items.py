import helpers.import_helper as imph

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
        imph.import_app().stop()