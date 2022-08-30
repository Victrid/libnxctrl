from typing import Type

from .wrapper import NXWrapper


def get_backend(backend_name: str) -> Type[NXWrapper]:
    if backend_name == "nxbt":
        from .nxbt_wrapper import NXBTControl
        return NXBTControl
    elif backend_name == "mart1no":
        from .joycontrol_wrapper import Mart1noJoyControl
        raise NotImplementedError("Joycontrol support is not implemented.")
        # return Mart1noJoyControl
    elif backend_name == "poohl":
        from .joycontrol_wrapper import PoohlJoyControl
        raise NotImplementedError("Joycontrol support is not implemented.")
        # return PoohlJoyControl
    else:
        raise ValueError("Unknown backend: {}".format(backend_name))
