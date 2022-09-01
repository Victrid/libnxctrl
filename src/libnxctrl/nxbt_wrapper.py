from typing import Union

from .nxbt.nxbt import Buttons as NXBT_Buttons, Nxbt, PRO_CONTROLLER, find_devices_by_alias
from .wrapper import Button, NXWrapper


def check_bluetooth_address(address: str) -> None:
    """Check the validity of a given Bluetooth MAC address

    :param address: A Bluetooth MAC address
    :type address: str
    :raises ValueError: If the Bluetooth address is invalid
    """

    address_bytes = len(address.split(":"))
    if address_bytes != 6:
        raise ValueError("Invalid Bluetooth address")


def get_reconnect_target(reconnect: bool, address: str):
    if reconnect:
        reconnect_target = find_devices_by_alias("Nintendo Switch")
    elif address:
        check_bluetooth_address(address)
        reconnect_target = address
    else:
        reconnect_target = None

    return reconnect_target


class NXBTControl(NXWrapper):
    button_map = {
        Button.A:             NXBT_Buttons.A,
        Button.B:             NXBT_Buttons.B,
        Button.X:             NXBT_Buttons.X,
        Button.Y:             NXBT_Buttons.Y,
        Button.DPAD_UP:       NXBT_Buttons.DPAD_UP,
        Button.DPAD_DOWN:     NXBT_Buttons.DPAD_DOWN,
        Button.DPAD_LEFT:     NXBT_Buttons.DPAD_LEFT,
        Button.DPAD_RIGHT:    NXBT_Buttons.DPAD_RIGHT,
        Button.SHOULDER_L:    NXBT_Buttons.L,
        Button.SHOULDER_R:    NXBT_Buttons.R,
        Button.SHOULDER_ZL:   NXBT_Buttons.ZL,
        Button.SHOULDER_ZR:   NXBT_Buttons.ZR,
        Button.L_STICK_PRESS: NXBT_Buttons.L_STICK_PRESS,
        Button.R_STICK_PRESS: NXBT_Buttons.R_STICK_PRESS,
        Button.HOME:          NXBT_Buttons.HOME,
        Button.CAPTURE:       NXBT_Buttons.CAPTURE,
        Button.MINUS:         NXBT_Buttons.MINUS,
        Button.PLUS:          NXBT_Buttons.PLUS,
        Button.JCL_SR:        NXBT_Buttons.JCL_SR,
        Button.JCL_SL:        NXBT_Buttons.JCL_SL,
        Button.JCR_SR:        NXBT_Buttons.JCR_SR,
        Button.JCR_SL:        NXBT_Buttons.JCR_SL
        }

    def __init__(self, press_duration_ms: int = 50, reconnect: bool = False, address: str = None):
        reconnect_target = get_reconnect_target(reconnect, address)
        super().__init__(press_duration_ms=press_duration_ms)
        self.nx = Nxbt()

        # Get a list of all available Bluetooth adapters
        adapters = self.nx.get_available_adapters()
        # Prepare a list to store the indexes of the
        # created controllers.
        controller_idxs = []
        # Loop over all Bluetooth adapters and create
        # Switch Pro Controllers
        for i in range(0, len(adapters)):
            index = self.nx.create_controller(
                    PRO_CONTROLLER,
                    adapter_path=adapters[i],
                    reconnect_address=reconnect_target
                    )
            controller_idxs.append(index)

        # Select the last controller for input
        self.controller_idx = controller_idxs[-1]

    def connect(self):
        self.nx.wait_for_connection(self.controller_idx)

    def button_hold(self, button: Button, duration_ms: int):
        self.nx.press_buttons(controller_index=self.controller_idx,
                              buttons=[self.button_map[button]],
                              down=duration_ms / 1000,
                              block=True
                              )

    def series_press(self, button_names: list[Union[Button, tuple[Button, int]]]):
        button_list = []
        for button in button_names:
            if isinstance(button, tuple):
                button_press = "{} {}s\n {}s".format(self.button_map[button[0]],
                                                     button[1] / 1000,
                                                     self.press_duration_ms / 1000
                                                     )
            elif isinstance(button, Button):
                button_press = "{} {}s\n {}s".format(self.button_map[button],
                                                     self.press_duration_ms / 1000,
                                                     self.press_duration_ms / 1000
                                                     )
        macro = "\n".join(button_list)
        print(macro)
        self.nx.macro(self.controller_idx, macro, block=True)

    def disconnect(self):
        pass
