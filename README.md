# libnxctrl

Python Library Emulating Nintendo Switch Controllers

## Installation

There are multiple backends: nxbt and splatplost USB. The nxbt backend can only be used on Linux, while the splatplost
USB backend can be used on Linux and Windows.

```bash
pip install libnxctrl[nxbt]
pip install libnxctrl[usb]
```

## Usage

If running libnxctrl as a linux bluetooth daemon, for example, on a raspberry Pi which doesn't have a GUI interface, you
can run with the following command:

```bash
libnxctrl --host 0.0.0.0 --port 15973
```

Use splatplost and select Remote Backend to connect to the daemon. For example, if you access your raspberry Pi
from `192.168.1.123` and set the port to `12345`, fill the `Remote Server` field with `http://192.168.1.123:12345`.