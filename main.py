from debug_tools.I2C_device_tester import I2CDeviceTester
from app.application import Application
import lib.ugit as ugit
# Create a ModuleConnectionTester object
I2C_tester = I2CDeviceTester(scl_pin=22, sda_pin=21)

# Check the connection
I2C_tester.check_display_connection()


# Create an OTAUpdater object
ugit.pull_all()
# Create an app object
app = Application()

# Initialize the app
app.initialize()
#test comment for ugit update
# Start the app
app.start()

# Update the app
app.update()
