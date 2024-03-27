import helpers.import_helper as imph

class MenuItem:
    def __init__(self):
        self.display_text = ""

    def command(self):
        raise NotImplementedError("Subclasses should implement this!")
    
class BackMenuItem(MenuItem):
    def __init__(self):
        self.display_text = "Back"
    
    def command(self):
        stm = imph.import_app().get_object("msm", "update")
        prev_state = stm.get_previous_state()
        stm.change_state(prev_state)

class ExitMenuItem(MenuItem):
    def __init__(self):
        self.display_text = "Exit"
    
    def command(self):
        imph.import_app().stop()