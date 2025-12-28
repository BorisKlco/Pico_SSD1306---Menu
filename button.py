from machine import Pin
import time

class Button:
    def __init__(self, pin_num, name):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.name = name
        self.last_press_time = 0
        self.debounce_delay = 200 # milliseconds to ignore repeat presses

    def is_pressed(self):
        current_time = time.ticks_ms()
        # Check if button is LOW (pressed) and if enough time has passed
        if self.pin.value() == 0:
            if time.ticks_diff(current_time, self.last_press_time) > self.debounce_delay:
                self.last_press_time = current_time
                return True
        return False
