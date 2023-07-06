# Blackmagic USB Control - Python

Controlling Blackmagic cameras via USB provides a number of advantages over Bluetooth control:

- No need to authenticate control systems: if the control system is connected to a camera via a USB connection, it has full control of the camera automatically without the need for authentication. Bluetooth pairing, by contrast, may be inadvertently reset - which then requires a new pairing to be established
- Better granularity of control: in testing it was possible to set focus to specific absolute values when Bluetooth only allowed incremental focus changes
- Better event reporting: for example USB control provides notification of when precise focus setting has completed

The [Blackmagic Cameras Code Samples](https://www.blackmagicdesign.com/uk/developer/product/camera) provided by [Blackmagic Design](https://www.blackmagicdesign.com/) include a sample Swift / Mac OS application for controlling Blackmagic cameras via a USB connection. In order to provide USB control of Blackmagic cameras for non-Mac-OS platforms, this project was created. It consists of a file-by-file and line-by-line code conversion of the USB control elements of Blackmagic's original Swift sample application into Python.  

The code has been successfully tested on a Raspberry Pi Zero W running Python 3.10 connected via USB to a Blackmagic Pocket Cinema Camera 6K with Sigma 18-35AF lens.

## Using the code
Instantiate an instance of `CameraControlInterface` from within a USB context:
```
from CameraControlInterface import *

with usb1.USBContext() as usbcontext:
    with CameraControlInterface(usbcontext) as cameracontrol:

```
Then call a particular function of `CameraControlInterface` from within the `CameraControlInterface` context:
```
from CameraControlInterface import *

with usb1.USBContext() as usbcontext:
    with CameraControlInterface(usbcontext) as cameracontrol:
        cameracontrol.onFocusPullSetInt(30000)
```
To see a list of available functions for `CameraControlInterface`, view `CameraControlInterface.py`

## Client Server
Within the `clientserver` folder, the two files `client.html` and `server.py` provide a simple demonstration of a client-server camera control system for controlling a Blackmagic camera via USB. 

- `server.py` should be run on a device with a USB connection to a Blackmagic camera
- `client.html` should be run on any web browser with an internet connection to the device running `server.py`. 

The demo client-server application uses a constant websocket connection to send client requests to the server, eg *Change focus*, and to receive camera notifications from the server, eg *ISO has changed*. To view the camera notifications from the browser, open a Javascript console.

## Python Version
The library uses the new `match case` available in Python 3.10 so Python >= 3.10 should be used. Alternatively, replace all `match case` instances with the appropriate `if elif` construction for Python < 3.10

## Installation
Create a Python 3.10 virtual environment from within `Blackmagic-USB`:
```
cd Blackmagic-USB
which python3.10
virtualenv -p [path-to-python3.10] venv
source venv/bin/activate
```
Install relevant Python libraries:
```
pip install -r requirements.txt
```

## Disclaimer
This is a *first pass* code conversion to demonstrate the principle of making a USB connection to Blackmagic cameras using Python. It has not been rigorously tested and is provided as-is for other developers to use and/or improve.

To contact the author, email [haselwimmer@gmail.com](haselwimmer@gmail.com)

Please note: This project is in no way affiliated with Blackmagic Design. All trademarks are property of their respective owners

