from debug_tools.I2C_device_tester import I2CDeviceTester
from machine import ADC, Pin
import time

# Create a ModuleConnectionTester object
I2C_tester = I2CDeviceTester(scl_pin=22, sda_pin=21)

# Check the connection
I2C_tester.check_display_connection()

adc_y = ADC(Pin(36))  # Assuming Pin 33 for Y-axis

adc_y.atten(ADC.ATTN_11DB)

while True:
    x_value = adc_y.read()

    print("X: ", x_value)
    time.sleep(2)