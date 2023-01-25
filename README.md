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

```
Usage: roku <options>

Options:
  --log-level [debug|info|error]  Log level (default: debug)
  --timeout INTEGER               length of time in seconds to keep listening
                                  for devices, default 60s
  -h, --help                      Show this message and exit.
```
Also part of the package is a utility called discover that performs network discovery of all
devices that respond to the SSDP request.
```
Usage: discover
```
Example output from discover:
~~~
$ discover 
2023-01-25 12:55:03,876 INFO     discovering ...
2023-01-25 12:55:03,877 INFO     discovery thread running
2023-01-25 12:55:03,880 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'upnp:rootdevice', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::upnp:rootdevice', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,881 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'urn:schemas-upnp-org:device:InternetGatewayDevice:1', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::urn:schemas-upnp-org:device:InternetGatewayDevice:1', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,881 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'urn:schemas-upnp-org:device:WANConnectionDevice:1', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::urn:schemas-upnp-org:device:WANConnectionDevice:1', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,881 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'urn:schemas-upnp-org:device:WANDevice:1', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::urn:schemas-upnp-org:device:WANDevice:1', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,881 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,882 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'urn:schemas-upnp-org:service:WANIPConnection:1', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::urn:schemas-upnp-org:service:WANIPConnection:1', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,882 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'urn:schemas-upnp-org:service:WANPPPConnection:1', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::urn:schemas-upnp-org:service:WANPPPConnection:1', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,882 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'urn:schemas-upnp-org:service:Layer3Forwarding:1', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c::urn:schemas-upnp-org:service:Layer3Forwarding:1', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:03,883 INFO     discovered: {'CACHE-CONTROL': 'max-age=120', 'ST': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c', 'USN': 'uuid:67d10bb0-9729-4a3f-8bb6-c2491237430c', 'EXT': '', 'SERVER': 'TP-Link/TP-LINK UPnP/1.1 MiniUPnPd/1.8', 'LOCATION': 'http://192.168.0.1:1900/ejbqw/rootDesc.xml', 'OPT': '"http://schemas.upnp.org/upnp/1/0/"; ns=01', '01-NLS': '1', 'BOOTID.UPNP.ORG': '1', 'CONFIGID.UPNP.ORG': '1337'}
2023-01-25 12:55:17,069 INFO     discovered: {'Cache-Control': 'max-age=3600', 'ST': 'upnp:rootdevice', 'USN': 'uuid:28000000-0000-1000-8008-44d878c2f084::upnp:rootdevice', 'Ext': '', 'Server': 'Roku/11.5.0 UPnP/1.0 Roku/11.5.0', 'LOCATION': 'http://192.168.0.172:8060/', 'WAKEUP': 'MAC=cc:a1:2b:6a:c5:cf;Timeout=10'}
2023-01-25 12:55:17,070 INFO     discovered: {'Cache-Control': 'max-age=3600', 'ST': 'roku:ecp', 'USN': 'uuid:roku:ecp:X000008HLY9X', 'Ext': '', 'Server': 'Roku/11.5.0 UPnP/1.0 Roku/11.5.0', 'LOCATION': 'http://192.168.0.172:8060/', 'device-group.roku.com': '016D31572B73AFE542A4', 'WAKEUP': 'MAC=cc:a1:2b:6a:c5:cf;Timeout=10'}
2023-01-25 12:55:17,070 INFO     discovered: {'Cache-Control': 'max-age=3600', 'ST': 'urn:dial-multiscreen-org:service:dial:1', 'USN': 'uuid:28000000-0000-1000-8008-44d878c2f084::urn:dial-multiscreen-org:service:dial:1', 'Ext': '', 'Server': 'Roku/11.5.0 UPnP/1.0 Roku/11.5.0', 'LOCATION': 'http://192.168.0.172:8060/dial/dd.xml', 'WAKEUP': 'MAC=cc:a1:2b:6a:c5:cf;Timeout=10'}
2023-01-25 12:55:32,161 INFO     discovered: {'Cache-Control': 'max-age=3600', 'ST': 'upnp:rootdevice', 'USN': 'uuid:296c0018-500b-1099-8029-64e0030354d9::upnp:rootdevice', 'Ext': '', 'Server': 'Roku/11.5.0 UPnP/1.0 Roku/11.5.0', 'LOCATION': 'http://192.168.0.103:8060/', 'WAKEUP': 'MAC=64:e0:03:03:54:d9;Timeout=10'}
2023-01-25 12:55:32,162 INFO     discovered: {'Cache-Control': 'max-age=3600', 'ST': 'roku:ecp', 'USN': 'uuid:roku:ecp:YK00HD760105', 'Ext': '', 'Server': 'Roku/11.5.0 UPnP/1.0 Roku/11.5.0', 'LOCATION': 'http://192.168.0.103:8060/', 'device-group.roku.com': '016D31572B73AFE542A4', 'WAKEUP': 'MAC=64:e0:03:03:54:d9;Timeout=10'}
2023-01-25 12:55:32,162 INFO     discovered: {'Cache-Control': 'max-age=3600', 'ST': 'urn:dial-multiscreen-org:service:dial:1', 'USN': 'uuid:296c0018-500b-1099-8029-64e0030354d9::urn:dial-multiscreen-org:service:dial:1', 'Ext': '', 'Server': 'Roku/11.5.0 UPnP/1.0 Roku/11.5.0', 'LOCATION': 'http://192.168.0.103:8060/dial/dd.xml', 'WAKEUP': 'MAC=64:e0:03:03:54:d9;Timeout=10'}
2023-01-25 12:56:03,910 INFO     stopping discovery thread
~~~

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
The application gui will start in "discovering ..." mode. 
After a period of time, network and device dependent, a list of Roku devices will appear.
The power button dynamically reflects the current power state of the Roku device. During initial discovery and re-discovery on a communication execption, the user-interface controls are disabled. Under a periodic (re)-discovery (every App.DISCOVER_INTERVAL - 5 minutes) the user interface controls remain enabled. The discover button will start a discovery thread unless one is already running. The currently selected Roku's power state is refreshed every App.POWER_UPDATE_INTERVAL (10 seconds).

![image info](./src/roku_remote/images/roku_remote.png)
![image info](./src/roku_remote/images/roku_remote2.png)
![image info](./src/roku_remote/images/roku_remote3.png)

# Keyboard Guide
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
| Home         	| Home          	|
| Escape       	| Back          	|
| Return       	| Select        	|

# Channel Ribbon
The channel ribbon contains images for each known channel. To select a channel to be displayed on the Roku, select it by clickig the mouse. The ribbon scrolls horizontally. I determined these by brute force requesting from my roku devices using a bash [script](./scripts/find_channels_by_brute_force.sh):
~~~
#!/bin/bash
mkdir temp
for i in {0..1000000}
do
    wget -q http://192.168.0.103:8060/query/icon/$i -O temp/chan$i.jpeg
    if [ $(expr $i % 1000) == "0" ]
    then
        echo $i
        find temp/ -size 0 -exec rm {} \;
        find temp/ ! -size 0 -print
    fi
done
find temp/ -size 0 -exec rm {} \;
~~~
The channel ribbon is created with the src/roku_remote/images/\*.jpeg files. You can remove chan\<id\>.jpeg images from the src/roku_remote/images/ folder that you don't want and they will no longer appear in the ribbon when it gets created.
See my example [script](./scripts/remove_unwanted_channels.sh) to do that.
Similarly, you can add your own chan\<id\>.jpeg image for a channel that you are aware of.
Here's a table of all the channel ids I know:
| Channel ID 	| Name    | Image  |
|------------	| ------  | ------ |
| 12          | Netflix | <img src="src/roku_remote/images/chan12.jpeg" width="75"> |
| 13          | Prime Video | <img src="src/roku_remote/images/chan13.jpeg" width="75">|
| 837         | YouTube | <img src="src/roku_remote/images/chan837.jpeg" width="75">|
| 2016          | Crackle | <img src="src/roku_remote/images/chan2016.jpeg" width="75">|
| 2285          | Hulu | <img src="src/roku_remote/images/chan2285.jpeg" width="75">|
| 14362          | Amazon Music | <img src="src/roku_remote/images/chan14362.jpeg" width="75">|
| 15985          | Play on Roku | <img src="src/roku_remote/images/chan15985.jpeg" width="75">|
| 19977          | Spotify | <img src="src/roku_remote/images/chan19977.jpeg" width="75">|
| 22297          | Spotify (again) | <img src="src/roku_remote/images/chan22297.jpeg" width="75">|
| 23353          | PBS | <img src="src/roku_remote/images/chan23353.jpeg" width="75">|
| 27536          | CBS News | <img src="src/roku_remote/images/chan27536.jpeg" width="75">|
| 31012          | Roku Vudu Store | <img src="src/roku_remote/images/chan31012.jpeg" width="75">|
| 31440          | Paramount + | <img src="src/roku_remote/images/chan31440.jpeg" width="75">|
| 34376          | ESPN | <img src="src/roku_remote/images/chan34376.jpeg" width="75">|
| 43465          | fuboTV | <img src="src/roku_remote/images/chan43465.jpeg" width="75">|
| 43508          | fuboTV (again) | <img src="src/roku_remote/images/chan43465.jpeg" width="75">|
| 43735          | unknown | <img src="src/roku_remote/images/chan43735.jpeg" width="75">|
| 54383          | DFP Ads | <img src="src/roku_remote/images/chan54383.jpeg" width="75">|
| 55545          | unknown | <img src="src/roku_remote/images/chan55545.jpeg" width="75">|
| 58484          | unknown | <img src="src/roku_remote/images/chan58484.jpeg" width="75">|
| 61322          | HBOmax | <img src="src/roku_remote/images/chan61322.jpeg" width="75">|
| 62675          | WCNC+ | <img src="src/roku_remote/images/chan62675.jpeg" width="75">|
| 72916          | GO! | <img src="src/roku_remote/images/chan72916.jpeg" width="75">|
| 74519          | pluto(tv) | <img src="src/roku_remote/images/chan74519.jpeg" width="75">|
| 83669          | NCAA March Madness Live | <img src="src/roku_remote/images/chan83669.jpeg" width="75">|
| 98832          | Roku Developers | <img src="src/roku_remote/images/chan98832.jpeg" width="75">|
| 109022          | unknown | <img src="src/roku_remote/images/chan109022.jpeg" width="75">|
| 122409          | kanopy | <img src="src/roku_remote/images/chan122409.jpeg" width="75">|
| 130644          | KARTOON channel! | <img src="src/roku_remote/images/chan130644.jpeg" width="75">|
| 151908          | Roku Channel | <img src="src/roku_remote/images/chan151908.jpeg" width="75">|
| 154157          | TNT | <img src="src/roku_remote/images/chan154157.jpeg" width="75">|
| 155883          | My Channel | <img src="src/roku_remote/images/chan155883.jpeg" width="75">|
| 173735          | Ecosystem | <img src="src/roku_remote/images/chan173735.jpeg" width="75">|
| 194485          | Survey Channel | <img src="src/roku_remote/images/chan194485.jpeg" width="75">|
| 250045          | My Channel (again) | <img src="src/roku_remote/images/chan250045.jpeg" width="75">|
| 260537          | Google Interactice Media Ads | <img src="src/roku_remote/images/chan260537.jpeg" width="75">|
| 262399          | unknown (chromium?) | <img src="src/roku_remote/images/chan262399.jpeg" width="75">|
| 265831          | Olympic Channel | <img src="src/roku_remote/images/chan265831.jpeg" width="75">|
| 272343          | My Channel (again) | <img src="src/roku_remote/images/chan272343.jpeg" width="75">|
| 278897          | unknown | <img src="src/roku_remote/images/chan278897.jpeg" width="75">|
| 291097          | Disney+ | <img src="src/roku_remote/images/chan291097.jpeg" width="75">|
| 291685          | Streaming Cities | <img src="src/roku_remote/images/chan291685.jpeg" width="75">|
| 295059          | Roku Developers (again) | <img src="src/roku_remote/images/chan295059.jpeg" width="75">|
| 551012          | AppleTV | <img src="src/roku_remote/images/chan551012.jpeg" width="75">|
| 557456          | CobaltLib | <img src="src/roku_remote/images/chan557456.jpeg" width="75">|
| 562859          | My Channel (again) | <img src="src/roku_remote/images/chan562859.jpeg" width="75">|
| 586995          | Airplay | <img src="src/roku_remote/images/chan586995.jpeg" width="75">|
| 594971          | My Channel (again) | <img src="src/roku_remote/images/chan594971.jpeg" width="75">|
| 596080          | Roku Developers (again) | <img src="src/roku_remote/images/chan596080.jpeg" width="75">|
| 596759          | TCL Channel Movies, Cartoons & TV | <img src="src/roku_remote/images/chan596759.jpeg" width="75">|
| 600835          | unknown | <img src="src/roku_remote/images/chan600835.jpeg" width="75">|
| 611444          | RUM | <img src="src/roku_remote/images/chan611444.jpeg" width="75">|
| 611688          | Roku NetPing | <img src="src/roku_remote/images/chan611688.jpeg" width="75">|
| 615685          | freevee | <img src="src/roku_remote/images/chan615685.jpeg" width="75">|
| 631123          | Happy Summer | <img src="src/roku_remote/images/chan631123.jpeg" width="75">|
| 631467          | CLoud SDK | <img src="src/roku_remote/images/chan631467.jpeg" width="75">|
| 633458          | Voice Help | <img src="src/roku_remote/images/chan633458.jpeg" width="75">|
| 639619          | My Channel (again) | <img src="src/roku_remote/images/chan639619.jpeg" width="75">|
| 659410          | Launcher | <img src="src/roku_remote/images/chan659410.jpeg" width="75">|
| 680626          | Dynamic | <img src="src/roku_remote/images/chan680626.jpeg" width="75">|
 
# User Interface Controls:
| Button | Function |
| ------ | -------- | 
| <img src="src/roku_remote/images/power_red.png" width="50" height="50"> | Power off |
| <img src="src/roku_remote/images/power_green.png" width="50" height="50"> | Power on |
| <img src="src/roku_remote/images/discover.png" width="50" height="50"> | Discover devices |
| <img src="src/roku_remote/images/back.png" width="75" height="50"> | Go back |
| <img src="src/roku_remote/images/guide.png" width="75" height="50"> | Guide |
| <img src="src/roku_remote/images/rocker_up.png" width="50" height="50"> | Up |
| <img src="src/roku_remote/images/rocker_down.png" width="50" height="50"> | Down |
| <img src="src/roku_remote/images/rocker_left.png" width="50" height="50"> | Left |
| <img src="src/roku_remote/images/rocker_right.png" width="50" height="50"> | Right |
| <img src="src/roku_remote/images/instant_replay.png" width="75" height="50"> | Instant Replay |
| <img src="src/roku_remote/images/info.png" width="75" height="50"> | Info / Options |
| <img src="src/roku_remote/images/headphones.png" width="75" height="50"> | no function as yet |
| <img src="src/roku_remote/images/rev.png" width="75" height="50"> | Rewind |
| <img src="src/roku_remote/images/play.png" width="75" height="50"> | Play / Pause |
| <img src="src/roku_remote/images/forward.png" width="75" height="50"> | Fast Forward |
| <img src="src/roku_remote/images/volume_mute.png" width="75" height="50"> | Volume Mute |
| <img src="src/roku_remote/images/volume_down.png" width="75" height="50"> | Volume Down |
| <img src="src/roku_remote/images/volume_up.png" width="75" height="50"> | Volume Up |
| <img src="src/roku_remote/images/channel_ribbon.png" width="150" height="50"> | Channel Ribbon, click image of channel to open on Roku |

