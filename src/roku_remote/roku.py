import requests
from urllib.parse import urlparse, quote

from lxml import objectify
import logging
from strenum import StrEnum

logger = logging.getLogger("main.roku")
class Roku:
    
    class Key(StrEnum):
        power_on = "PowerOn"
        power_off = "PowerOff"
        home = "Home"
        rev = "Rev"
        fwd = "Fwd"
        play = "Play"
        select = "Select"
        left = "Left"
        right = "Right"
        down = "Down"
        up = "Up"
        back = "Back"
        guide = "LiveTV"
        instant_replay = "InstantReplay"
        info = "Info"
        backspace = "Backspace"
        search = "Search"
        enter = "Enter"
        volume_down = "VolumeDown"
        volume_mute = "VolumeMute"
        volume_up = "VolumeUp"
        channel_up = "ChannelUp"
        channel_down = "ChannelDown"
        input_tuner = "InputTuner"
        input_hdmi1 = "InputHDMI1"
        input_hdmi2 = "InputHDMI2"
        input_hdmi3 = "InputHDMI3"
        input_hdmi4 = "InputHDMI4"
        input_av1 = "InputAV1"
        
    def __init__(self, dict) -> None:
        self.api_url = urlparse(dict['LOCATION']).geturl()
        self.device_info = None
        self.name = self.get_device_info("friendly-device-name")

    def log_response(self, method, roku, url, status_code, text):
        if not (status_code == 200 or status_code == 202):
            logger.error(f"error in {method} roku {roku} url {url} status {status_code} {text}")
        else:
            logger.info(f"{method} roku {roku} url {url} status {status_code} {text}")

    # actions
    def send_keypress(self, key):
        url = self.api_url + "keypress/" + key
        response = requests.post(url)
        self.log_response("send_keypress", self.name, url, response.status_code, response.text)

    def send_keydown(self, key):
        url = self.api_url + "keydown/" + key
        response = requests.post(url)
        self.log_response("send_keydown", self.name, url, response.status_code, response.text)

    keyup = "keyup"
    def send_keyup(self, key):
        url = self.api_url + "keyup/" + key
        response = requests.post(url)
        self.log_response("send_keyup", self.name, url, response.status_code, response.text)

    def send_launch_channel(self, id):
        url = self.api_url + "launch" + "/" + id
        response = requests.post(url)
        self.log_response("launch", self.name, url, response.status_code, response.text)

    # key actions
    def send_power_on(self):
        self.send_keypress(Roku.Key.power_on)

    def send_power_off(self):
        self.send_keypress(Roku.Key.power_off)

    def send_key_home(self):
        self.send_keypress(Roku.Key.home)

    def send_key_rev(self):
        self.send_keypress(Roku.Key.rev)

    def send_key_fwd(self):
        self.send_keypress(Roku.Key.fwd)

    def send_key_play(self):
        self.send_keypress(Roku.Key.play)

    def send_key_select(self):
        self.send_keypress(Roku.Key.select)

    def send_key_left(self):
        self.send_keypress(Roku.Key.left)

    def send_key_right(self):
        self.send_keypress(Roku.Key.right)

    def send_key_down(self):
        self.send_keypress(Roku.Key.down)

    def send_key_up(self):
        self.send_keypress(Roku.Key.up)

    def send_key_back(self):
        self.send_keypress(Roku.Key.back)

    def send_key_guide(self):
        self.send_keypress(Roku.Key.guide)

    def send_key_instant_replay(self):
        self.send_keypress(Roku.Key.instant_replay)

    def send_key_info(self):
        self.send_keypress(Roku.Key.info)

    def send_key_backspace(self):
        self.send_keypress(Roku.Key.backspace)

    def send_key_search(self):
        self.send_keypress(Roku.Key.search)

    def send_key_enter(self):
        self.send_keypress(Roku.Key.enter)

    def send_key_volume_down(self):
        self.send_keypress(Roku.Key.volume_down)

    def send_key_volume_mute(self):
        self.send_keypress(Roku.Key.volume_mute)

    def send_key_volume_up(self):
        self.send_keypress(Roku.Key.volume_up)

    def send_key_channel_up(self):
        self.send_keypress(Roku.Key.channel_up)
        
    def send_key_channel_down(self):
        self.send_keypress(Roku.Key.channel_down)

    def send_key_input_tuner(self):
        self.send_keypress(Roku.Key.input_tuner)

    def send_key_input_hdmi1(self):
        self.send_keypress(Roku.Key.input_hdmi1)

    def send_key_input_hdmi2(self):
        self.send_keypress(Roku.Key.input_hdmi2)

    def send_key_input_hdmi3(self):
        self.send_keypress(Roku.Key.input_hdmi3)

    def send_key_input_hdmi4(self):
        self.send_keypress(Roku.Key.input_hdmi4)

    def send_key_input_av1(self):
        self.send_keypress(Roku.Key.input_av1)

    def send_key_headphones(self):
        pass

    def send_key_power(self):
        if self.is_power_on():
            self.send_power_off()
        else:
            self.send_power_on()

    def send_char(self, char, keysym):
        if len(char):
            if char in "@#$&+=:;,?/ ":
                char = quote(char, safe="")
                self.send_keypress(f"Lit_{char}")
                return
            if char.isprintable():
                self.send_keypress(f"Lit_{char}")
                return

        match keysym:
            case 'BackSpace':
                self.send_key_backspace()
            case 'Delete':
                self.send_key_backspace()
            case 'Up':
                self.send_key_up()
            case 'Down':
                self.send_key_down()
            case 'Left':
                self.send_key_left()
            case 'Right':
                self.send_key_right()
            case 'Home' | 'Escape':
                self.send_key_home()
            case 'Pause':
                self.send_key_play()
            case 'Return':
                self.send_key_select()

    # utilities
    def is_power_on(self):
        value = self.get_device_info("power-mode")
        if value == "PowerOn":
            return True
        else:
            return False

    def is_tv(self):
        return self.get_device_info("is-tv")

    def is_stick(self):
        return self.get_device_info("is-stick")

    def get_description(self):
        if self.is_tv():
            return "TV"
        elif self.is_stick():
            return "Stick"
        return "unknown"

    def get_device_info(self, key):
        if self.device_info is None or key == "power-mode":
            url = self.api_url + "query/device-info"
            try:
                response = requests.get(url)
                self.device_info = objectify.fromstring(response.content)
            except Exception as ex:
                logger.error(f"exception {ex} in get_device_info({key})")
                raise(ex)
            except:
                logger.error(f"unknown error in get_device_info()")
        return self.device_info[key]

    def get_name(self):
        return self.name

    def get_api_url(self):
        return self.api_url


