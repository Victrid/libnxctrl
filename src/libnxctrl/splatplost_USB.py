import ctypes
import re
from enum import IntEnum, IntFlag
from time import sleep
from typing import Optional

import serial

from .wrapper import Button, NXWrapper


class USBInput(ctypes.Structure):
    _fields_ = [("index", ctypes.c_uint32), ("ctrl", ctypes.c_uint8), ("buttons", ctypes.c_uint16),
                ("dpad", ctypes.c_uint8), ("lx", ctypes.c_uint8), ("ly", ctypes.c_uint8), ("rx", ctypes.c_uint8),
                ("ry", ctypes.c_uint8), ("pressTick", ctypes.c_uint32), ]


class SplatplostUSBControl(NXWrapper):
    support_combo = True

    class SPUButton(IntFlag):
        """
        This value is fixed, do not change it.
        """
        NONE = 0x00,
        SWITCH_Y = 0x01,
        SWITCH_B = 0x02,
        SWITCH_A = 0x04,
        SWITCH_X = 0x08,
        SWITCH_L = 0x10,
        SWITCH_R = 0x20,
        SWITCH_ZL = 0x40,
        SWITCH_ZR = 0x80,
        SWITCH_MINUS = 0x100,
        SWITCH_PLUS = 0x200,
        SWITCH_LCLICK = 0x400,
        SWITCH_RCLICK = 0x800,
        SWITCH_HOME = 0x1000,
        SWITCH_CAPTURE = 0x2000,

    class SPU_DPAD(IntEnum):
        """
        This value is fixed, do not change it.
        """
        CENTER = 0x08,
        UP = 0x00,
        RIGHT = 0x02,
        DOWN = 0x04,
        LEFT = 0x06,
        RIGHT_UP = 0x01,
        RIGHT_DOWN = 0x03,
        LEFT_UP = 0x07,
        LEFT_DOWN = 0x05,

    STICK_MIN = 0
    STICK_CENTER = 128
    STICK_MAX = 255

    def __init__(self, serial_port: str, press_duration_ms: int = 30):
        super().__init__(press_duration_ms)

        self.serial_port = serial_port
        self.serial: Optional[serial.Serial] = None
        self.poll_rate = 10
        self.report_idx = 0

        self.wait_time = 20

    def send_report(self, report: USBInput):
        report.index = self.report_idx
        self.serial.write(report)
        acknowledge_info = self.serial.readline().decode("ASCII").strip()
        ack_format = r"###ACK ([0-9]+)###"
        match = re.match(ack_format, acknowledge_info)
        if match:
            if self.report_idx != int(match.group(1)):
                raise Exception("Report index mismatch")
        else:
            raise Exception("Invalid acknowledge info")
        self.report_idx += 1

    def connect(self):
        # TODO: Implement connection check
        self.serial = serial.Serial(self.serial_port, 115200)
        for _ in range(50):
            self.button_press(Button.SHOULDER_L | Button.SHOULDER_R)

    def button_name_to_SPUButton(self, button_name: Button) -> SPUButton:
        button_map = {
            Button.A:             self.SPUButton.SWITCH_A,
            Button.B:             self.SPUButton.SWITCH_B,
            Button.X:             self.SPUButton.SWITCH_X,
            Button.Y:             self.SPUButton.SWITCH_Y,
            Button.SHOULDER_L:    self.SPUButton.SWITCH_L,
            Button.SHOULDER_R:    self.SPUButton.SWITCH_R,
            Button.SHOULDER_ZL:   self.SPUButton.SWITCH_ZL,
            Button.SHOULDER_ZR:   self.SPUButton.SWITCH_ZR,
            Button.L_STICK_PRESS: self.SPUButton.SWITCH_LCLICK,
            Button.R_STICK_PRESS: self.SPUButton.SWITCH_RCLICK,
            Button.HOME:          self.SPUButton.SWITCH_HOME,
            Button.CAPTURE:       self.SPUButton.SWITCH_CAPTURE,
            Button.MINUS:         self.SPUButton.SWITCH_MINUS,
            Button.PLUS:          self.SPUButton.SWITCH_PLUS,
            }

        new_button = self.SPUButton.NONE
        for button, internal_button in button_map.items():
            if button_name & button:
                new_button = internal_button | new_button

        return new_button

    def button_name_to_DPAD(self, button_name: Button) -> SPU_DPAD:
        dpad_map = {
            Button.DPAD_UP:    self.SPU_DPAD.UP,
            Button.DPAD_DOWN:  self.SPU_DPAD.DOWN,
            Button.DPAD_LEFT:  self.SPU_DPAD.LEFT,
            Button.DPAD_RIGHT: self.SPU_DPAD.RIGHT,
            }

        new_button = self.SPU_DPAD.CENTER
        for button, dpad_button in dpad_map.items():
            # Only allow one dpad button to be pressed at a time
            if button_name & button:
                new_button = dpad_button

        return new_button

    def button_hold(self, button_name: Button, duration_ms: int):
        report = USBInput(buttons=self.button_name_to_SPUButton(button_name).value,
                          dpad=self.button_name_to_DPAD(button_name).value,
                          lx=self.STICK_CENTER,
                          ly=self.STICK_CENTER,
                          rx=self.STICK_CENTER,
                          ry=self.STICK_CENTER,
                          pressTick=1 if duration_ms // self.poll_rate == 0 else duration_ms // self.poll_rate,
                          )
        self.send_report(report)
        report = USBInput(buttons=0,
                          dpad=self.SPU_DPAD.CENTER.value,
                          lx=self.STICK_CENTER,
                          ly=self.STICK_CENTER,
                          rx=self.STICK_CENTER,
                          ry=self.STICK_CENTER,
                          pressTick=1 if duration_ms // self.poll_rate == 0 else duration_ms // self.poll_rate,
                          )
        self.send_report(report)

    def button_press(self, button_name: Button):
        self.button_hold(button_name, self.press_duration_ms)

    def disconnect(self):
        self.serial.close()
