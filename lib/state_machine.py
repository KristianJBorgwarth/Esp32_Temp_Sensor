import gc
import helpers.import_helper as imph

class IState():
    def __init__(self):
        if type(self) == IState:
            raise Exception("<IState> cannot be instantiated")
        self.oled = imph.import_app().get_object("oled")
        self.input_handler = imph.import_app().get_object("input")
        self.menu_items = None
        self.selected_item = 0
        self.menu_name = ""
        
    def enter(self):
        raise NotImplementedError("Subclasses should implement this!")

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

        self.oled.print_menu(self.menu_items, self.selected_item, self.menu_name)

    def exit(self):
        self.oled.clear_screen()
        gc.collect()

class StateMachine:
    def __init__(self, state: IState):
        self._current_state = state
        self._history_stack = []
        self._current_state.enter()

    def update(self):
        self._current_state.execute()

    def change_state(self, new_state: IState):
        if self._current_state == new_state:
            return
        if self._current_state is not None:
            self._history_stack.append(self._current_state)
            self._current_state.exit()
            gc.collect()

        self._current_state = new_state
        self._current_state.enter()

    def go_back(self):
        if len(self._history_stack) == 0:
            return
        self._current_state.exit()
        self._current_state = self._history_stack.pop()
        self._current_state.enter()

    def get_state(self):
        return self._current_state


