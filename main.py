from debug_tools.I2C_device_tester import I2CDeviceTester

# Create a ModuleConnectionTester object
I2C_tester = I2CDeviceTester(scl_pin=22, sda_pin=21)

# Check the connection
I2C_tester.check_display_connection()