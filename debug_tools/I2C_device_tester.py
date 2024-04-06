from machine import Pin, SoftI2C

class I2CDeviceTester:
    def __init__(self, scl_pin, sda_pin):
        self.scl_pin = scl_pin
        self.sda_pin = sda_pin
        self.i2c = SoftI2C(scl=Pin(scl_pin), sda=Pin(sda_pin))

    def check_display_connection(self):
        devices = self.i2c.scan()
        if devices:
            for device in devices:
                print("I2C device found at address: 0x{0:02x}".format(device))
        else:
            print("No I2C device found")