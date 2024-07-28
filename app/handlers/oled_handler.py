import drivers.SSD1306 as SSD1306
from machine import Pin, SoftI2C

class OLEDHandler:

    def __init__(self):
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.oled_width = 128
        self.oled_height = 64
        self.char_width = 8
        self.oled = SSD1306.SSD1306_I2C(self.oled_width, self.oled_height, i2c)

    # This method will print the message to the OLED screen
    def print_to_screen(self, message):
        self.oled.fill(0)  # Clear the display first
        lines = message.split('\n')  # Split the message into lines at each '\n'
    
        processed_lines = []
        for line in lines:
            # Further split each line into words to respect max_chars_per_line
            words = line.split(' ')
            current_line = ''
            for word in words:
                # Check if adding the next word exceeds the line width
                if len(current_line) + len(word) <= 28:
                    current_line += (word + ' ')
                else:
                    # Line is full, add to processed lines and start a new one
                    processed_lines.append(current_line.strip())
                    current_line = word + ' '
            processed_lines.append(current_line.strip())  # Add the last or only line of the segment

        # Now, print each processed line to the OLED
        for i, processed_line in enumerate(processed_lines):
            if i < 8:  # Limit to the display's ability to show lines
                self.oled.text(processed_line, 0, i * 10)
    
        self.oled.show()

    def print_menu(self, items, selected_item, menu_title):
        self.oled.fill(0)
        self.display_menu_title(menu_title)
        self.display_menu_items(items, selected_item)
        self.oled.show()
    
    def display_menu_title(self, title):
        text_length_pixels = len(title) * self.char_width
        text_start_pos = (self.oled_width // 2) - (text_length_pixels // 2)
        self.oled.text(title, text_start_pos, 0)
        self.draw_line(10)

    def display_menu_items(self, items, selected_item):
        start_y_pos = 12
        for i, item in enumerate(items):
            x_pos = self.center_text_position(item.display_text)
            if i == selected_item:
                self.oled.text(">", x_pos - self.char_width, start_y_pos + i * 10)
            self.oled.text(item.display_text, x_pos, start_y_pos + i * 10)

    def center_text_position(self, text):
        text_length_pixels = len(text) * self.char_width
        text_start_pos = (self.oled_width // 2) - (text_length_pixels // 2)
        return text_start_pos

    def draw_line(self, y, color = 1):
        for x in range(self.oled_width):
            self.oled.pixel(x, y, color)

    def clear_screen(self):
        self.oled.fill(0)
        print("Screen cleared")
        self.oled.show()