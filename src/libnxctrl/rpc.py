import base64
import pickle
from typing import Union
from xmlrpc.client import ServerProxy

from .wrapper import Button, NXWrapper


class RemoteControlServer:
    def __init__(self):
        try:
            from .nxbt_wrapper import NXBTControl
        except ImportError:
            raise ImportError("NXBT is not available.")
        self.control = None

    def init(self, pickled_args: str) -> int:
        if type(pickled_args) != str:
            pickled_args = str(pickled_args)
        from .nxbt_wrapper import NXBTControl
        args = pickle.loads(base64.b64decode(pickled_args))
        print(args)
        self.control = NXBTControl(**args)
        return 0

    def connect(self) -> int:
        self.control.connect()
        return 0

    def button_hold(self, pickled_args: str) -> int:
        if type(pickled_args) != str:
            pickled_args = str(pickled_args)
        args = pickle.loads(base64.b64decode(pickled_args))
        self.control.button_hold(**args)
        return 0

    def button_press(self, pickled_args: str) -> int:
        if type(pickled_args) != str:
            pickled_args = str(pickled_args)
        args = pickle.loads(base64.b64decode(pickled_args))
        self.control.button_press(**args)
        return 0

    def series_press(self, pickled_args: str) -> int:
        if type(pickled_args) != str:
            pickled_args = str(pickled_args)
        args = pickle.loads(base64.b64decode(pickled_args))
        self.control.series_press(**args)
        return 0

    def disconnect(self) -> int:
        self.control.disconnect()
        self.control = None
        return 0


class RemoteControlClient(NXWrapper):
    def __init__(self, conn_str: str, press_duration_ms: int = 50, delay_ms: int = 120):
        super().__init__(press_duration_ms, delay_ms)
        self.host = conn_str
        self.control = ServerProxy(self.host)
        self.conn_args = {
            "press_duration_ms": press_duration_ms,
            "delay_ms":          delay_ms
            }
        self.control.init(base64.b64encode(pickle.dumps(self.conn_args)))

    def connect(self):
        self.control.connect()

    def button_hold(self, button_name: Button, duration_ms: int):
        self.control.button_hold(
                base64.b64encode(pickle.dumps({"button_name": button_name, "duration_ms": duration_ms}))
                )

    def button_press(self, button_name: Button):
        self.control.button_press(base64.b64encode(pickle.dumps({"button_name": button_name})))

    def series_press(self, button_names: list[Union[Button, tuple[Button, int]]]):
        self.control.series_press(base64.b64encode(pickle.dumps({"button_names": button_names})))

    def disconnect(self):
        self.control.disconnect()
        self.control = None
