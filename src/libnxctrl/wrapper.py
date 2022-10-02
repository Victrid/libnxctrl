from abc import abstractmethod
from enum import Flag, auto
from typing import Union


class Button(Flag):
    A = auto()
    B = auto()
    X = auto()
    Y = auto()
    DPAD_UP = auto()
    DPAD_DOWN = auto()
    DPAD_LEFT = auto()
    DPAD_RIGHT = auto()
    L_STICK_PRESS = auto()
    R_STICK_PRESS = auto()
    SHOULDER_L = auto()
    SHOULDER_R = auto()
    SHOULDER_ZL = auto()
    SHOULDER_ZR = auto()
    HOME = auto()
    CAPTURE = auto()
    MINUS = auto()
    PLUS = auto()
    JCL_SR = auto()
    JCL_SL = auto()
    JCR_SR = auto()
    JCR_SL = auto()


class NXWrapper:
    support_combo = False

    def combo_supported(self):
        return self.support_combo

    def __init__(self, press_duration_ms: int = 50, delay_ms: int = 120):
        self.press_duration_ms = press_duration_ms
        self.delay_ms = delay_ms

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
