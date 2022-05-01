import configparser
import os

from libqtile import layout

from _get_screensize import _get_resolution


path_home = os.path.expanduser("~")
path_config = os.path.join(path_home, ".config/qtile/config.ini")
# For debugging only.
if not os.path.exists(path_config):
    path_config = "config.ini"  # When executing from the directory.

config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read(path_config)

screen_width, screen_height = _get_resolution()
default_margin = int(screen_width*16/2560)

border_focus = config["layout"]["border_focus"]
border_normal = config["layout"]["border_normal"]
border_width = config["layout"].getint("border_width")
margin = config["layout"].getint("margin", fallback=default_margin)
ratio = config["layout"].getfloat("ratio")

default_config = {
    'border_focus': border_focus,
    'border_normal': border_normal,
    'border_width': border_width,
    'margin': margin,
    'ratio': ratio,
}

layouts = [
    layout.Max(**default_config),
    layout.MonadTall(**default_config),
]

# Possible layouts:
# layout.Stack(num_stacks=2),
# layout.Bsp(),
# layout.Columns(),
# layout.Floating(),
# layout.Matrix(),
# layout.MonadWide(),
# layout.RatioTile(),
# layout.Tile(),
# layout.TreeTab(),
# layout.VerticalTile(),
# layout.Zoomy(),
