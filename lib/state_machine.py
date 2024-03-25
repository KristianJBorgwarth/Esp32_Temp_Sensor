from abc import ABC, abstractmethod

class IState(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def exit(self):
        pass

class StateMachine(ABC):
    @abstractmethod
    def __init__(self, state: IState):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def change_state(self, new_state: IState):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def get_previous_state(self):
        pass


