import drivers.SSD1306 as SSD1306
from machine import Pin, SoftI2C

class OLEDHandler:

    def __init__(self):
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        oled_width = 128
        oled_width = 64
        self.oled = SSD1306.SSD1306_I2C(oled_width, oled_width, i2c)

    # This method will print the message to the OLED screen
    def print_to_screen(self, message):
        self.oled.fill(0)
        max_chars_per_line = 7
        words = message.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars_per_line:
                current_line += (word + ' ')
            else:
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)  # Add the last line
        
        for i, line in enumerate(lines):
            if i < 8:  # Prevent adding more lines than the display can show (adjust based on your display's capability)
                self.oled.text(line.strip(), 0, i * 10)
        
        self.oled.show()

    def print_menu(self, items, selected_item):
        self.oled.fill(0)
        for i, item in enumerate(items):
            if i == selected_item:
                self.oled.text(">" + item.display_text, 0, i * 10)
            else:
                self.oled.text(item.display_text, 0, i * 10)
        self.oled.show()