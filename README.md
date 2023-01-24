# roku
### Description
roku is a GUI application that is a remote control for Roku devices.

roku is written in Python.

### About
The application uses [SSDP](https://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol) and [RokuECP](https://developer.roku.com/docs/developer-program/debugging/external-control-api.md)
to discover and control Roku devices on the network and displays a user-interface resembling a remote control.
This allows you to:
* select the device to control
* select the video input
* navigate the on-screen user-interface
* click the various buttons to send commands to the roku
* use the keyboard to send keystrokes in search boxes


# Keyboard
The user interface has keyboard support, so you can type in search fields etc. Other keys with functions are:
| Keyboard Key 	| Roku Function 	|
|--------------	|---------------	|
| Backspace    	| Backspace     	|
| Delete       	| Backspace     	|
| Cursor Up    	| Up            	|
| Cursor Down  	| Down          	|
| Cursor Right 	| Right         	|
| Cursor Left  	| Left          	|
| Pause        	| Play/Pause    	|
| Home         	| Home/Back     	|
| Escape       	| Home/Back     	|
| Return       	| Select        	|

# Channel Ribbon
The channel ribbon contains images for each known channel. To select a channel to be displayed on the Roku, select it by clickig the mouse. The ribbon scrolls horizontally and it contains all the channel ids I know of which are:
| Channel ID 	| Name    | Image  |
|------------	| ------  | ------ |
| 12          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg){width=75 height=50} |
| 13          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 837         | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 2016          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 2285          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 14362          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 5985          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 19977          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 22297          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 3353          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 27536          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 31012          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 31440          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| |34376          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 43465          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 43508          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 43735          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 54383          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 55545          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 58484          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 61322          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 62675          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 72916          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 74519          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 83669          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 98832          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 109022          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 122409          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 130644          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 151908          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 154157          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 155883          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 173735          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 194485          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 250045          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 260537          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 262399          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 265831          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 272343          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 278897          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 291097          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 291685          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 295059          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 551012          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 557456          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 562859          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 586995          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 594971          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 596080          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 596759          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 600835          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 611444          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 611688          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 615685          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 631123          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 631467          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 633458          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 639619          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 659410          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
| 680626          | Netflix | ![image info](./src/roku_remote/images/chan12.jpeg) |
 
```
Usage: roku <options>

Options:
  --log-level [debug|info|error]  Log level (default: debug)
  --timeout INTEGER               length of time in seconds to keep listening
                                  for devices, default 60s
  -h, --help                      Show this message and exit.


Also part of the package is a utility called discover that performs network discovery of all
devices that respond to the SSDP request.

Usage: discover
```
The application gui will start in "discovering ..." mode:

![image info](./src/roku_remote/images/roku_remote.png)

After a period of time, network and device dependent, a list of Roku devices will appear.
The power button dynamically reflects the current power state of the Roku device:

![image info](./src/roku_remote/images/roku_remote2.png)
![image info](./src/roku_remote/images/roku_remote3.png)

To build the application:
```
python -m build
```
To install/reinstall the wheel:
```
pip install dist/*.whl [--force-reinstall]
```
or to install as editable
```
pip install -e .
```
