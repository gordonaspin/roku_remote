import logging
import os
import re
import tkinter as tk
import tkinter.ttk as ttk
from fnmatch import fnmatch
from queue import Queue

import Pmw
from importlib_resources import files
from PIL import Image, ImageTk

import roku_remote.images
from roku_remote.discover import discover
from roku_remote.roku import Roku

logger = logging.getLogger("main.app")

class App:
    REGSITER_ROKU_EVENT = "<<RegisterRoku>>"
    COMBOBOX_SELECTED_EVENT = "<<ComboboxSelected>>"
    bgcolor = "#521c86"
    troughcolor = "#662d91"
    DISCOVER_INTERVAL = 5*60*1000
    POWER_UPDATE_INTERVAL = 10*1000
    activebgcolor = bgcolor

    def __init__(self, window):
        """creates the main window object, creates widgets, arranges to grid and wires
        up the combobox selection and roku registration events"""
        self.image_path = files(roku_remote.images)
        self.window = window
        Pmw.initialise(window)
        self.title = self.window.title("Roku Remote")
        self.window.configure(bg=self.bgcolor)
        self.window.resizable(False, False)
        self.window.iconphoto(False, tk.PhotoImage(file=f"{self.image_path}/roku_remote.png"))

        self.registration_queue = Queue()
        self.rokus = []
        self.roku = None

        self._create_widgets()
        self._layout_widgets()
        self._disable_widgets()

        self.window.bind(self.REGSITER_ROKU_EVENT, self.register_roku)
        self.window.after(App.DISCOVER_INTERVAL, self.discover)
        self.window.bind('<KeyPress>', self.on_key_press)
        self.device_combobox.bind(self.COMBOBOX_SELECTED_EVENT, self.device_selection_changed)
        self.input_combobox.bind(self.COMBOBOX_SELECTED_EVENT, self.input_selection_changed)

    def on_key_press(self, event):
        logger.debug(f"on_key_press code:{event.keycode}: code.hex:{event.keycode:02x} char:{event.char}")
        if self.roku:
            self.roku.send_char(event.char, event.keysym)

    def register_roku(self, event):
        """called by the Tk.mainloop when a REGISTER_ROKU_EVENT has been posted from the discovery thread
        pops the Roku from the registration queue, checks the comobox to see if we have registered any
        roku yet, if so checks whether this is a known roku, if a new roku then appends to the roku array.
        If this is the first registration, posts a selection change event for the combobox and sets the current
        selection to 0, the first roku"""
        roku = self.registration_queue.get()
        roku_name = roku.get_name()
        values = self.device_combobox['values']
        current = self.device_combobox.current()
        logger.debug(f"registering Roku {roku_name}, current selected is {current} values {values}")
        if (values) == ("discovering...",): # see _create_widgets where the combobox is created
            values = ()
            current = -1
        if roku_name in values:
            logger.info(f"Roku {roku_name} is already registered")
            return
        self.rokus.append(roku)
        values = values + (roku_name,)
        self.device_combobox['values'] = values
        if current == -1:
            self._enable_widgets()
            self.device_combobox.current(0)
            self.device_selection_changed(event)
            self.window.after(App.POWER_UPDATE_INTERVAL, self.update_power_button_state)

    def register_device(self, dict):
        """called from discovery thread as a callback
        creates a new Roku object from the dictionary, posts to the registration queue
        and posts an event to the Tk.mainloop in order to add the Roku to the combobox"""
        roku = Roku(dict)
        logger.info(f"registering {roku.get_description()} {roku.get_name()} {roku.get_device_info('friendly-model-name')} at {roku.get_api_url()}")
        self.registration_queue.put(Roku(dict))
        self.window.event_generate(self.REGSITER_ROKU_EVENT)

    def update_power_button_state(self, user_action=False):
        """called every App.POWER_UPDATE_INTERVAL seconds from the Tk.mainloop
        to check power state of device and update power button image.
        TODO: Research if Roku sends network events via SSDP, or websockets"""
        if self.roku:
            try:
                power = self.roku.is_power_on()
            except Exception as ex:
                logger.error(f"{self.roku.get_name}: exception {ex} in update_power_button, resetting...")
                self.discover(True, True)
                return
            logger.debug(f"{self.roku.get_name()}: power is {'on' if power else 'off'}")
            self.power_btn.set_power(power)
            if user_action == False:
                logger.debug(f"{self.roku.get_name()}: resetting self.window.after")
                self.window.after(App.POWER_UPDATE_INTERVAL, self.update_power_button_state)

    def power_button(self):
        """sends power button message to selected roku device"""
        self.roku.send_key_power()
        self.update_power_button_state(True)

    def discover(self, force=False, user_action=False):
        """starts a discovery thread when the user clicks the discover button or upon
        an exception getting power button state """
        logger.debug(f"discover(force={force}, user_action={user_action})")
        if force:
            self.rokus.clear()
            self.roku = None
            self.reset_combobox()
            self._disable_widgets()
        discover("roku:ecp", self.register_device, force) 
        if user_action == False:
            self.window.after(App.DISCOVER_INTERVAL, self.discover)

    def input_selection_changed(self, event):
        """event handler when user selects new input from combobox"""
        selection = self.input_combobox.get()
        if self.roku is not None:
            match selection:
                case "HDMI-1":
                    self.roku.send_key_input_hdmi1()
                case "HDMI-2":
                    self.roku.send_key_input_hdmi2()
                case "HDMI-3":
                    self.roku.send_key_input_hdmi3()
                case "HDMI-4":
                    self.roku.send_key_input_hdmi4()
                case "Tuner":
                    self.roku.send_key_input_tuner()
                case "AV-1":
                    self.roku.send_key_input_av1()
        self.window.focus_set()
        

    def device_selection_changed(self, event):
        """event handler when user selects new device from combobox"""
        selection = self.device_combobox.get()
        for roku in self.rokus:
            if roku.get_name() == selection:
                self.roku = roku
                self.update_power_button_state(True)
        self.window.focus_set()

    def reset_combobox(self):
        self.device_combobox['values'] = ("discovering...",)
        self.device_combobox.current(0)

    def _assemble_settables(self):
        settables = self.window.winfo_children()
        for w in settables:
            settables += w.winfo_children()
        return filter(lambda w: w.__class__.__name__ in ['Canvas', 'Combobox'], settables)

    def _disable_widgets(self):
        for widget in self._assemble_settables():
            try:
                widget["state"] = tk.DISABLED
            except:
                pass

    def _enable_widgets(self):
        for widget in self._assemble_settables():
            try:
                widget["state"] = 'readonly'
            except:
                pass

    def _create_widgets(self):
        """creates all the UI widgets"""
        # Combobox
        if False:
            self.window.option_add("*TCombobox*Listbox.background", App.bgcolor)
            self.window.option_add("*TCombobox*Listbox.foreground", 'white')
            self.window.option_add("*TCombobox*Listbox.selectBackground", App.bgcolor)
            self.window.option_add("*TCombobox*Listbox.selectForeground", 'white')

        if False:
            style = ttk.Style()
            style.configure("TCombobox", arrowcolor='white', background=App.bgcolor, foreground='black', fieldbackground=App.bgcolor, selectbackground=App.bgcolor, selectforeground="black")

        if False:
            for state in ['readonly', 'disabled', 'active', 'focus', 'invalid', 'pressed', 'selected']:
                style.map('TCombobox', arrowcolor=[(state, 'white')])
                style.map('TCombobox', background=[(state, App.bgcolor)])
                style.map('TCombobox', foreground=[(state, 'black')])
                style.map('TCombobox', fieldbackground=[(state, App.bgcolor)])
                style.map('TCombobox', selectbackground=[(state, App.bgcolor)])
                style.map('TCombobox', selectforeground=[(state, 'black')])

        self.device_combobox = ttk.Combobox(state="readonly")
        balloon = Pmw.Balloon(self.device_combobox)
        balloon.bind(self.device_combobox, "choose device")
        balloon.configure(relmouse="both")
        self.reset_combobox()

        # Buttons: each button is a clickable image with alpha-channel laying on a canvas
        self.power_btn          = App.PowerButton(self, self.window, "power", f"{self.image_path}/power_red.png", lambda event: self.btn_clicked(self.power_button), 50, 50, f"{self.image_path}/power_green.png")
        self.discover_btn       = App.Button(self, self.window, "discover", f"{self.image_path}/discover.png", lambda event: self.discover(True, True), 50, 50)

        self.back_btn           = App.Button(self, self.window, "back", f"{self.image_path}/back.png", lambda event: self.btn_clicked(self.roku.send_key_back), 75, 50)
        self.guide_btn          = App.Button(self, self.window, "guide", f"{self.image_path}/guide.png", lambda event: self.btn_clicked(self.roku.send_key_guide), 75, 50)
        self.home_btn           = App.Button(self, self.window, "home", f"{self.image_path}/home.png", lambda event: self.btn_clicked(self.roku.send_key_home), 75, 50)

        self.rocker_nw          = App.Button(self, self.window, None, f"{self.image_path}/rocker_nw.png", None, 78, 78)
        self.up_btn             = App.Button(self, self.window, "up", f"{self.image_path}/rocker_up.png", lambda event: self.btn_clicked(self.roku.send_key_up), 78, 78)
        self.rocker_ne          = App.Button(self, self.window, None, f"{self.image_path}/rocker_ne.png", None, 78, 78)
        self.left_btn           = App.Button(self, self.window, "left", f"{self.image_path}/rocker_left.png", lambda event: self.btn_clicked(self.roku.send_key_left), 78, 78)
        self.select_btn         = App.Button(self, self.window, "select", f"{self.image_path}/rocker_center.png", lambda event: self.btn_clicked(self.roku.send_key_select), 78, 78)
        self.right_btn          = App.Button(self, self.window, "right", f"{self.image_path}/rocker_right.png", lambda event: self.btn_clicked(self.roku.send_key_right), 78, 78)
        self.rocker_sw          = App.Button(self, self.window, None, f"{self.image_path}/rocker_sw.png", None, 78, 78)
        self.down_btn           = App.Button(self, self.window, "down", f"{self.image_path}/rocker_down.png", lambda event: self.btn_clicked(self.roku.send_key_down), 78, 78)
        self.rocker_se          = App.Button(self, self.window, None, f"{self.image_path}/rocker_se.png", None, 78, 78)

        self.instant_replay_btn = App.Button(self, self.window, "instant replay", f"{self.image_path}/instant_replay.png", lambda event: self.btn_clicked(self.roku.send_key_instant_replay), 75, 50)
        self.info_btn           = App.Button(self, self.window, "info", f"{self.image_path}/info.png", lambda event: self.btn_clicked(self.roku.send_key_info), 75, 50)
        self.headphones_btn     = App.Button(self, self.window, "headphones", f"{self.image_path}/headphones.png", lambda event: self.btn_clicked(self.roku.send_key_headphones), 75, 50)
        self.rev_btn            = App.Button(self, self.window, "rewind", f"{self.image_path}/rev.png", lambda event: self.btn_clicked(self.roku.send_key_rev), 75, 50)
        self.play_btn           = App.Button(self, self.window, "play/pause", f"{self.image_path}/play.png", lambda event: self.btn_clicked(self.roku.send_key_play), 75, 50)
        self.fwd_btn            = App.Button(self, self.window, "forward", f"{self.image_path}/forward.png", lambda event: self.btn_clicked(self.roku.send_key_fwd), 75, 50)
        self.volume_up_btn      = App.Button(self, self.window, "volume up", f"{self.image_path}/volume_up.png", lambda event: self.btn_clicked(self.roku.send_key_volume_up), 75, 50)
        self.volume_down_btn    = App.Button(self, self.window, "volume down", f"{self.image_path}/volume_down.png", lambda event: self.btn_clicked(self.roku.send_key_volume_down), 75, 50)
        self.volume_mute_btn    = App.Button(self, self.window, "volume mute", f"{self.image_path}/volume_mute.png", lambda event: self.btn_clicked(self.roku.send_key_volume_mute), 75, 50)

        self.input_combobox = ttk.Combobox(state="readonly", width=5)
        balloon = Pmw.Balloon(self.input_combobox)
        balloon.bind(self.device_combobox, "select input")
        balloon.configure(relmouse="both")
        self.input_combobox['values'] = ("input","HDMI-1","HDMI-2","HDMI-3","HDMI-4","Tuner","AV-1")
        self.input_combobox.current(0)

        self.channel_frame = App.ScrollableFrame(self.window, 225, 50)

        self.channel_buttons = []
        for r, d, files in os.walk(self.image_path):
            for f in files:
                if fnmatch(f, "*.jpeg"):
                    path = os.path.join(r, f)
                    channel_id = re.search(r'\d+', f).group()
                    button = App.Button(self, self.channel_frame.scrollable_frame, channel_id, path, None, 75, 50)
                    self.channel_buttons.append(button)
        self.channel_buttons.sort(key=lambda button: int(button.name), reverse=False)
        pass

    def _layout_widgets(self):
        """lays out all the widgets in a 3 column, multirow grid"""
        # Use grid to layout widgets
        self.device_combobox            .grid(row=0, columnspan=3, padx=0, pady=10)

        self.power_btn.canvas           .grid(row=1, column=0, padx=0, pady=10)#, stick=tk.NSEW)
        self.input_combobox             .grid(row=1, column=1, padx=0, pady=10)
        self.discover_btn.canvas        .grid(row=1, column=2, padx=0, pady=10)#, stick=tk.NSEW)

        self.back_btn.canvas            .grid(row=2, column=0, padx=5, pady=10, stick=tk.NSEW)
        self.guide_btn.canvas           .grid(row=2, column=1, padx=0, pady=10, stick=tk.NSEW)
        self.home_btn.canvas            .grid(row=2, column=2, padx=5, pady=10, stick=tk.NSEW)

        self.rocker_nw.canvas           .grid(row=3, column=0, padx=0, pady=0, stick=tk.SE)
        self.up_btn.canvas              .grid(row=3, column=1, padx=0, pady=0, stick=tk.S)
        self.rocker_ne.canvas           .grid(row=3, column=2, padx=0, pady=0, stick=tk.SW)

        self.left_btn.canvas            .grid(row=4, column=0, padx=0, pady=0, stick=tk.E)
        self.select_btn.canvas          .grid(row=4, column=1, padx=0, pady=0, )#stick=tk.NSEW)
        self.right_btn.canvas           .grid(row=4, column=2, padx=0, pady=0, stick=tk.W)

        self.rocker_sw.canvas           .grid(row=5, column=0, padx=0, pady=0, stick=tk.NE)
        self.down_btn.canvas            .grid(row=5, column=1, padx=0, pady=0, stick=tk.N)
        self.rocker_se.canvas           .grid(row=5, column=2, padx=0, pady=0, stick=tk.NW,)

        self.instant_replay_btn.canvas  .grid(row=6, column=0, padx=5, pady=10, stick=tk.NSEW)
        self.info_btn.canvas            .grid(row=6, column=1, padx=0, pady=10, stick=tk.NSEW)
        self.headphones_btn.canvas      .grid(row=6, column=2, padx=5, pady=10, stick=tk.NSEW)
        
        self.rev_btn.canvas             .grid(row=7, column=0, padx=5, pady=10, stick=tk.NSEW)
        self.play_btn.canvas            .grid(row=7, column=1, padx=0, pady=10, stick=tk.NSEW)
        self.fwd_btn.canvas             .grid(row=7, column=2, padx=5, pady=10, stick=tk.NSEW)
        
        self.volume_mute_btn.canvas     .grid(row=8, column=0, padx=5, pady=10, stick=tk.NSEW)
        self.volume_down_btn.canvas     .grid(row=8, column=1, padx=0, pady=10, stick=tk.NSEW)
        self.volume_up_btn.canvas       .grid(row=8, column=2, padx=5, pady=10, stick=tk.NSEW)

        self.channel_frame              .grid(row=9, columnspan=3, padx=0, pady=10)
        i = 0
        for button in self.channel_buttons:
            button.canvas.grid(row=0, column=i)
            i += 1


    def btn_clicked(self, obj):
        """handles button clicks by either delegating to the button object's
        btn_clicked method if it exists, or by wiring based on the button object"""
        logger.debug(f"{__class__.__name__}.btn_clicked")
        if self.roku is None or obj is None:
            if self.roku is None:
                logger.debug(f"btn_clicked self.roku is None")
            if obj is None:
                logger.debug(f"btn_clicked obj is None")
            return
        try:
            obj()
        except Exception as ex:
            logger.debug(f"Exception {ex} App to handle function of button")
            obj.btn_clicked()

    class Button():
        """helper class to build button widgets based on canvases and images"""
        def __init__(self, app, window, name, image_path, onclick, x, y, alt_image_path=None):
            self.app = app
            self.name = name
            self.canvas = tk.Canvas(window, width=x, height=y, bd=0, borderwidth=0, highlightthickness=0, bg=App.bgcolor)
            self.img = ImageTk.PhotoImage(Image.open(image_path).resize((x,y)))
            if alt_image_path is not None:
                self.alt_img = ImageTk.PhotoImage(Image.open(alt_image_path).resize((x,y)))
            self.btn_img = self.canvas.create_image(self.canvas.winfo_reqwidth()/2, self.canvas.winfo_reqheight()/2, anchor=tk.CENTER, image=self.img)
            if name is not None:
                balloon = Pmw.Balloon(self.canvas)
                balloon.bind(self.canvas, name)
                balloon.configure(relmouse="both")
            if onclick is not None:
                self.onclick = onclick
                self.canvas.tag_bind(self.btn_img, "<Button-1>", self.onclick)
            else:
                if name is not None:
                    self.canvas.tag_bind(self.btn_img, "<Button-1>", self.btn_clicked)
        
        def btn_clicked(self, ev):
            logger.debug(f"Button.btn_clicked {self.name}")
            self.app.roku.send_launch_channel(self.name)

    class PowerButton(Button):
        """PowerButton subclass of Button to handle special case of changing image when power state changes"""
        def set_power(self, power):
            self.btn_img = self.canvas.create_image(self.canvas.winfo_reqwidth()/2, self.canvas.winfo_reqheight()/2, anchor=tk.CENTER, image=self.alt_img if power else self.img)
            self.canvas.tag_bind(self.btn_img, "<Button-1>", self.onclick)

    class ScrollableFrame(ttk.Frame):
        def __init__(self, container, width, height, *args, **kwargs):
            super().__init__(container, *args, **kwargs)
            canvas = tk.Canvas(self, width=width, height=height, borderwidth=0, highlightthickness=0)
            style=ttk.Style()
            style.configure('Horizontal.TScrollbar', troughcolor=App.troughcolor, background=App.bgcolor, bordercolor=App.bgcolor, arrowcolor="white")
            scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
            self.scrollable_frame = ttk.Frame(canvas, borderwidth=0)

            self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
            canvas.configure(xscrollcommand=scrollbar.set)
            canvas.grid(row=0, column=0)
            scrollbar.grid(row=1, column=0, sticky=tk.NSEW)
