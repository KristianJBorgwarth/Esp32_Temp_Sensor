import time
from umqtt.simple import MQTTClient
import machine 


class MqttHandler:
    def __init__(self):
        self.AZURE_IOT_HUB_HOSTNAME = "IoTCourseEsp32.azure-devices.net"
        self.AZURE_IOT_HUB_DEVICE_ID = "Esp32Temp"
        self.AZURE_IOT_HUB_DEVICE_SAS = "SharedAccessSignature sr=IoTCourseEsp32.azure-devices.net%2Fdevices%2FEsp32Temp&sig=%2BJG0oRcALV1RGsTwOt8MISaHjbENWcs8QoXpPLYKBRA%3D&se=1712182295"
        self.USERNAME = self.AZURE_IOT_HUB_HOSTNAME + "/" + self.AZURE_IOT_HUB_DEVICE_ID + "/api-version=2018-06-30"
        self.PASSWORD = self.AZURE_IOT_HUB_DEVICE_SAS   
        self.MQTTCLIENT = MQTTClient(self.AZURE_IOT_HUB_DEVICE_ID, self.AZURE_IOT_HUB_HOSTNAME, user=self.USERNAME, password=self.PASSWORD, port=8883, keepalive=120, ssl=True)

    def connect(self):
        self.MQTTCLIENT.connect()
        print("Connected to Azure IoT Hub")
    
    def publish(self, message):
        self.MQTTCLIENT.publish(f"devices/{self.AZURE_IOT_HUB_DEVICE_ID}/messages/events/", message.encode())
        print("Published: " + message)
    