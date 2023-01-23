import logging
import tkinter as tk

import click

from roku_remote import __version__
from roku_remote.app import App
from roku_remote.discover import discover

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

@click.command(context_settings=CONTEXT_SETTINGS, options_metavar="<options>")
@click.option("--log-level", help="Log level (default: debug)", type=click.Choice(["debug", "info", "error"]), default="error")
@click.option("--timeout", help="length of time in seconds to keep listening for devices, default 60s", type=click.INT, default=60)

def main(timeout, log_level):
    """main python application entrypoint. Creates the Tk window, creates the App gui
    and starts the SSDP discovery thread passing the application registration callback"""
    format = "%(asctime)s %(levelname)-8s %(message)s"
    if log_level == "debug":
        level = logging.DEBUG
        format='%(asctime)s %(levelname)-8s %(funcName)-32s %(message)s'
    elif log_level == "info":
        level = logging.INFO
    elif log_level == "error":
        level = logging.ERROR

    logger = logging.getLogger("main")
    logger.setLevel(level)
    logging.basicConfig(format=format)

    logger.info(f"roku {__version__}")
    logger.info(f"looking for roku devices on network for {timeout} seconds ...")

    root = tk.Tk()
    app = App(root)
    discover("roku:ecp", app.register_device, force=False, timeout=timeout)
    root.mainloop()

if __name__ == "__main__":
    main()