from typing import Type

from .wrapper import NXWrapper


def get_available_backend() -> list[str]:
    available_backend = []
    try:
        # NXBT
        import dbus
        import flask
        import flask_socketio
        import eventlet
        import blessed
        import pynput
        import psutil
        import cryptography
        available_backend.append("nxbt")
    except ImportError:
        pass
    try:
        # Splatplost USB
        import serial
        available_backend.append("Splatplost USB")
    except ImportError:
        pass

    return available_backend


def get_backend(backend_name: str) -> Type[NXWrapper]:
    if backend_name not in get_available_backend():
        raise ValueError(f"Backend {backend_name} is not available.")
    if backend_name == "nxbt":
        from .nxbt_wrapper import NXBTControl
        return NXBTControl
    elif backend_name == "mart1no":
        raise NotImplementedError("Joycontrol support is not implemented.")
        # return Mart1noJoyControl
    elif backend_name == "poohl":
        raise NotImplementedError("Joycontrol support is not implemented.")
        # return PoohlJoyControl
    elif backend_name == "Splatplost USB":
        from .splatplost_USB import SplatplostUSBControl
        return SplatplostUSBControl
    else:
        raise ValueError(f"Backend {backend_name} is not available.")
