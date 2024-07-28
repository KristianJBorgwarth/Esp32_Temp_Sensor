from umqtt.simple import MQTTClient
import ujson
from app.menu.items.settings_menu_items import UpdateMenuItem
import gc
class MqttHandler:
    def __init__(self):
        self.AZURE_IOT_HUB_HOSTNAME = "SOME_HOST_NAME"
        self.AZURE_IOT_HUB_DEVICE_ID = "SOME_DEVICE_ID"
        self.AZURE_IOT_HUB_DEVICE_SAS = "SOME_SAS"
        self.USERNAME = self.AZURE_IOT_HUB_HOSTNAME + "/" + self.AZURE_IOT_HUB_DEVICE_ID + "/api-version=2018-06-30"
        self.PASSWORD = self.AZURE_IOT_HUB_DEVICE_SAS   
        self.MQTTCLIENT = MQTTClient(self.AZURE_IOT_HUB_DEVICE_ID, self.AZURE_IOT_HUB_HOSTNAME, user=self.USERNAME, password=self.PASSWORD, port=8883, keepalive=120, ssl=True)

    def connect(self):
        self.MQTTCLIENT.connect()
        print("Connected to Azure IoT Hub")
    
    def publish(self, message):
        try: 
            self.MQTTCLIENT.publish(f"devices/{self.AZURE_IOT_HUB_DEVICE_ID}/messages/events/", message.encode())
            print("Published: " + message)
        except Exception as e:
            print("Error in MQTT publish: " + str(e))
            self.MQTTCLIENT.connect()
        
    def subscribe(self):
        #Subscribe to C2D messages
        self.MQTTCLIENT.set_callback(self.on_message)
        self.MQTTCLIENT.subscribe(f"devices/{self.AZURE_IOT_HUB_DEVICE_ID}/messages/devicebound/#")
        
    def on_message(self, topic, message):
        message = message.decode('utf-8')
        print("Received message:{}".format(message))
        try:
            data = ujson.loads(message)
            if data.get("action")=="update":
                self.MQTTCLIENT.disconnect()
                print("Received update action")
                gc.collect()
                update = UpdateMenuItem()
                update.command()
        except Exception as e:
            print("Error in MQTT on_message: " + str(e))
            pass 
        
    def update(self):
        try:
            self.MQTTCLIENT.check_msg()
        except Exception as e:
            print("Error in MQTT update: " + str(e))
            self.MQTTCLIENT.connect()
        gc.collect()
            
    
