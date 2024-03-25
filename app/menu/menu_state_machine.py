
class MenuStateMachine:
    def __init__(self, state) -> None:
        self._current_state = state
        self._current_state.Enter()

    def ChangeState(self, state):
        if self._current_state != None:
            self._current_state.Exit()

        self._current_state = state
        self._current_state.Enter()


    def Update(self):
        if self._current_state != None:
            self._current_state.Execute()
