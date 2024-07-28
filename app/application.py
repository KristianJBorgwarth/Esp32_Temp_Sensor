import time
import gc
from app.handlers.oled_handler import OLEDHandler as oled
from lib.state_machine import StateMachine
from app.handlers.input_handler import InputHandler
from app.menu.states.main_menu import MainMenuState as MMS
from lib.wifi.wifi_manager import WifiManager
from app.handlers.mqtt_handler import MqttHandler
from app.handlers.temp_handler import TempHandler

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
        wfm = self.initialize_wifi()
        mqtt = self.initialize_mqtt()
        self.add_object("mqtt", mqtt, "update")
        self.add_object("cpm", wfm)
        self.add_object("input", InputHandler())
        self.add_object("temp_sensor", TempHandler())
        self.add_object("msm", StateMachine(MMS()), "update")

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
        time.sleep(1)
    
    def add_object(self, tag, obj, type = None):
        if type == "update":
            self._updateObjects[tag] = obj
        else:
            self._objects[tag] = obj

    def get_object(self, tag, type = None):
        if type == "update":
            return self._updateObjects[tag]
        else:
            return self._objects[tag]
    
    def delete_object(self, tag, type = None):
        if type == "update":
            del self._updateObjects[tag]
        else:
            del self._objects[tag]
        gc.collect()

    def initialize_wifi(self):
        wfm = WifiManager("ESP32_AP", "12345678")
        wfm.connect()
        return wfm
    
    def initialize_mqtt(self):
        mqtt = MqttHandler()
        mqtt.connect()
        mqtt.subscribe()
        return mqtt
    
    def clear_all_objects(self):
        self._objects.clear()
        self._updateObjects.clear()
        gc.collect()
        print("Bulk delete done")
    


    