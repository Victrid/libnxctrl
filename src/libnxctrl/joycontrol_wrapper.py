import asyncio
import os

from .wrapper import Button, NXWrapper


class Mart1noJoyControl(NXWrapper):
    def __init__(self, press_duration_ms: int = 50):
        from .mart1no_joycontrol.joycontrol.controller import Controller
        from .mart1no_joycontrol.joycontrol.device import HidDevice
        from .mart1no_joycontrol.joycontrol.memory import FlashMemory
        from .mart1no_joycontrol.joycontrol.protocol import controller_protocol_factory
        from .mart1no_joycontrol.joycontrol.server import create_hid_server
        super().__init__(press_duration_ms)
        if not os.geteuid() == 0:
            raise PermissionError('Script must be run as root!')
        hid = HidDevice(device_id=None)
        transport, protocol = asyncio.run(create_hid_server(
                controller_protocol_factory(Controller.from_arg("PRO_CONTROLLER"), spi_flash=FlashMemory()),
                ctl_psm=17,
                itr_psm=19
                )
                )
        controller_state = protocol.get_controller_state()
        self.transport = transport
        self.controller_state = controller_state

    def connect(self):
        asyncio.run(self.controller_state.connect())

    def button_hold(self, button: Button, duration_ms: int):
        from mart1no_joycontrol.joycontrol.controller_state import button_push
        # TODO get button name from enum
        raise NotImplementedError
        # asyncio.run(button_push(self.controller_state, button, sec=duration_ms / 1000))

    def disconnect(self):
        asyncio.run(self.transport.close())


class PoohlJoyControl(NXWrapper):
    def __init__(self, press_duration_ms: int = 50):
        from .Poohl_joycontrol.joycontrol.controller import Controller
        from .Poohl_joycontrol.joycontrol.device import HidDevice
        from .Poohl_joycontrol.joycontrol.memory import FlashMemory
        from .Poohl_joycontrol.joycontrol.protocol import controller_protocol_factory
        from .Poohl_joycontrol.joycontrol.server import create_hid_server
        super().__init__(press_duration_ms)
        if not os.geteuid() == 0:
            raise PermissionError('Script must be run as root!')
        hid = HidDevice(device_id=None)
        transport, protocol = asyncio.run(create_hid_server(
                controller_protocol_factory(Controller.from_arg("PRO_CONTROLLER"), spi_flash=FlashMemory()),
                ctl_psm=17,
                itr_psm=19
                )
                )
        controller_state = protocol.get_controller_state()
        self.transport = transport
        self.controller_state = controller_state

    def connect(self):
        asyncio.run(self.controller_state.connect())

    def button_hold(self, button: Button, duration_ms: int):
        from Poohl_joycontrol.joycontrol.controller_state import button_push
        # TODO get button name from enum
        raise NotImplementedError
        # asyncio.run(button_push(self.controller_state, button, sec=duration_ms / 1000))

    def disconnect(self):
        asyncio.run(self.transport.close())
