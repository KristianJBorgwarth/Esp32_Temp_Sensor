from drivers.SSD1306 import SSD1306 as ssd

class OledHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
            oled_width = 128
            oled_width = 64
            cls._instance.ssd_driver = ssd(i2c, oled_width, oled_width)
        return cls._instance

    def print_to_screen(self, message):
        self.ssd_driver.fill(0)
        max_chars_per_line = 15  # Adjust this based on your display and font size
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