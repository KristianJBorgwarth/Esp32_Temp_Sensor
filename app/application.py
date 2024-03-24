import time
from app.handlers.oled_handler import oled_handler as oled
import gc

class app: 
    _instance = None
    _isRunning = True
    _objectDict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self):
        print("Initializing the app")
        self.add_object("oled", oled())
        
    def start(self):
        print("Starting the app")

    def update(self):
        while(self._isRunning):
            print("Updating the app")
            time.sleep(1)

    def stop(self):
        self._isRunning = False
        print("Shutting down")
    
    def add_object(self, tag, obj):
        self._objectDict[tag] = obj

    def get_object(self, tag):
        return self._objectDict[tag]
    
    def delete_object(self, tag):
        del self._objectDict[tag]
        gc.collect()


    