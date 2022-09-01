from abc import abstractmethod
from enum import Enum
from typing import Union


class Button(Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    DPAD_UP = 4
    DPAD_DOWN = 5
    DPAD_LEFT = 6
    DPAD_RIGHT = 7
    L_STICK_PRESS = 8
    R_STICK_PRESS = 9
    SHOULDER_L = 10
    SHOULDER_R = 11
    SHOULDER_ZL = 12
    SHOULDER_ZR = 13
    HOME = 14
    CAPTURE = 15
    MINUS = 16
    PLUS = 17
    JCL_SR = 18
    JCL_SL = 19
    JCR_SR = 20
    JCR_SL = 21


class NXWrapper:
    def __init__(self, press_duration_ms: int = 50):
        self.press_duration_ms = press_duration_ms

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def button_hold(self, button_name: Button, duration_ms: int):
        """
        Hold a button for a certain duration.

        :param button_name: The name of the button to push.
        :param duration_ms: The duration in milliseconds.
        """
        pass

    def button_press(self, button_name: Button):
        """
        Press a button.

        :param button_name: The name of the button to push.
        """
        return self.button_hold(button_name, self.press_duration_ms)

    def series_press(self, button_names: list[Union[Button, tuple[Button, int]]]):
        """
        Press a series of buttons.
        :param button_names: A list of button names.
        """
        for button_name in button_names:
            if isinstance(button_name, tuple):
                self.button_hold(button_name[0], button_name[1])
            else:
                self.button_press(button_name)

    @abstractmethod
    def disconnect(self):
        pass

    # Context Manager
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        return False
