import _thread
import helpers.import_helper as imph
import esp32
import time

class TempHandler:
    def __init__(self):
        self.mqtt = imph.import_app().get_object("mqtt", "update")
        self.temperature = 0
        self.isRunning = False
    
    def measure_and_send(self):
        while self.isRunning:
            self.temperature = esp32.raw_temperature()
            self.temperature = self.convert_temp_to_celsius(self.temperature)
            self.mqtt.publish(str(self.temperature))
            time.sleep(1)

    def start(self):
        if not self.isRunning:
            self.isRunning = True
            _thread.start_new_thread(self.measure_and_send, ())
                
    def stop(self):
        self.isRunning = False

    def convert_temp_to_celsius(self, raw_temp):
        return (raw_temp - 32) * 5.0/9.0