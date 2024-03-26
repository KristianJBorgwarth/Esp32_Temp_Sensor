import time
import gc
from app.handlers.oled_handler import OLEDHandler as oled
from lib.state_machine import StateMachine
from app.handlers.input_handler import InputHandler
from app.states.main_menu import MainMenuState as MMS

class Application: 
    _instance = None
    _isRunning = True
    _objects: dict = {}
    _updateObjects: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self):
        print("Initializing the app")
        self.add_object("oled", oled())
        self.add_object("input", InputHandler())
        self.add_object("msm", StateMachine(MMS(self.get_object("oled"))), "update")

    def start(self):
        print("Starting the app")

    def update(self):
        while(self._isRunning):
            for obj in self._updateObjects.values():
                obj.update()
            time.sleep(0.1)
            
    def stop(self):
        self._isRunning = False
        print("Shutting down")
    
    def add_object(self, tag, obj, type = None):
        if type == "update":
            self._updateObjects[tag] = obj
        else:
            self._objects[tag] = obj

    def get_object(self, tag, type = None):
        if type == "update":
            print("trying to fetch object")
            return self._updateObjects[tag]
        else:
            return self._objects[tag]
    
    def delete_object(self, tag, type = None):
        if type == "update":
            del self._updateObjects[tag]
        else:
            del self._objects[tag]
        gc.collect()

    


    