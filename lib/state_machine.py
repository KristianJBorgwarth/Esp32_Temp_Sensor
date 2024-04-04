import gc
class IState():
    def __init__(self):
        if type(self) == IState:
            raise Exception("<IState> cannot be instantiated")

    def enter(self):
        raise NotImplementedError("Subclasses should implement this!")

    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")

    def exit(self):
        raise NotImplementedError("Subclasses should implement this!")

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


