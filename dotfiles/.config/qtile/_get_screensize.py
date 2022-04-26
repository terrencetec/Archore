import configparser
import os

from screeninfo import get_monitors


# Get home string
path_home = os.path.expanduser("~")

config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
path_config = os.path.join(path_home, ".config/qtile/config.ini")

# For debugging
if not os.path.exists(path_config):
    path_config = "config.ini"  # When executing from the directory.

config.read(path_config)

default_screen_width = config["monitor"].getint("width")
default_screen_height = config["monitor"].getint("height")

def _get_resolution():
    """Returns a tuple of screen width and height.
    """
    if len(get_monitors()) == 0:
        screen_width = default_screen_width 
        screen_height = default_screen_height
    else:
        for monitor in get_monitors():
            if monitor.is_primary:
                screen_width = monitor.width
                screen_height = monitor.height
                break
            else:
                screen_width = default_screen_width
                screen_height = default_screen_height
    return screen_width, screen_height
