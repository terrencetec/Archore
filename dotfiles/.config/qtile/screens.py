"""Setup screen, bar, and widgets.

Do not hardcode any configuration values in this file.
Instead, modify "config.ini".
"""
import os
import configparser

from _get_screensize import _get_resolution 

from libqtile import bar, widget, qtile
from libqtile.config import Screen
from libqtile.lazy import lazy

# Get home string
path_home = os.path.expanduser("~")

# Get monitor resolution
screen_width, screen_height = _get_resolution()

# Determine optimal sizes for the bar.
# For 2560x1440, my bar size was 32.
# Font size was 18, giving a ratio of font to bar size of 0.5625.
# Systray icon size has a multiplier of 3/4 so it was 24.
# Clock font size has a multiplier of 1/2 so it was 9.
default_barsize = int(screen_height/1440*32)
default_fontsize = int(default_barsize*0.5625)
default_iconsize = int(default_fontsize)
default_clock_fontsize = int(default_fontsize*2/3)

# Config
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
path_config = os.path.join(path_home, ".config/qtile/config.ini")

# For debugging
if not os.path.exists(path_config):
    path_config = "config.ini"  # When executing from the directory.

config.read(path_config)


# Parsing the config
bar_size = config["bar"].getint("size", fallback=default_barsize)
background = config["bar"]["background"]  # background color or the bar.
opacity = config["bar"].getfloat("opacity")  # opacity of the bar

# Default variables.
default_font = config["widget"]["font"]
default_fontsize = config["widget"].getint(
    "fontsize", fallback=default_fontsize)
default_foreground = config["widget"]["foreground"]
default_icon_path = os.path.join(path_home, ".config/qtile/icon.png")
if not os.path.exists(default_icon_path):
    default_icon_path = "icon.png"  # When executing from the directory.
    # For debug only.

# Required for config.py, somehow...
widget_defaults = {
    "font": default_font,
    "fontsize": default_fontsize,
    "foreground": default_foreground,
}


# Command for the rofi launcher.
def rofi_exit():
    qtile.cmd_spawn(os.path.join(path_home, ".config/rofi/rofi-exit.sh"))


widget_list = []

# Scan config and set up widgets.
if "image" in config.sections():
    margin = config["image"].getint("margin")
    icon_path = config["image"].get("icon_path", fallback=default_icon_path)
    widget_image = widget.Image(
        margin=margin, filename=icon_path,
        mouse_callbacks={"Button1": rofi_exit})
    widget_list.append(widget_image)

if "group_box" in config.sections():
    active_color = config["group_box"]["active_color"]
    block_highlight_text_color = config["group_box"].get(
        "block_highlight_text_color", fallback=default_foreground)
    borderwidth = config["group_box"].getint("borderwidth")
    highlight_method = config["group_box"]["highlight_method"]
    widget_groupbox = widget.GroupBox(
        active=active_color,
        block_highlight_text_color=block_highlight_text_color,
        borderwidth=borderwidth,
        highlight_method=highlight_method,
    )
    widget_list.append(widget_groupbox)

if "task_list" in config.sections():
    border_color = config["task_list"]["border_color"]
    unfocused_border_color = config["task_list"]["unfocused_border_color"]
    font = config["task_list"].get("font", fallback=default_font)
    margin = config["task_list"].getint("margin")
    max_title_width = config["task_list"].getint("max_title_width")
    padding = config["task_list"].getint("padding")
    rounded = config["task_list"].getboolean("rounded")
    widget_tasklist = widget.TaskList(
        border=border_color,
        unfocused_border=unfocused_border_color,
        font=font,
        margin=margin,
        max_title_width=max_title_width,
        padding=padding,
        rounded=rounded
    )
    widget_list.append(widget_tasklist)

if "current_layout" in config.sections():
    fmt = config["current_layout"]["fmt"]
    widget_currentlayout = widget.CurrentLayout(
        fmt=fmt,
    )
    widget_list.append(widget_currentlayout)

if "prompt" in config.sections():
    widget_list.append(widget.Prompt())

if "systray" in config.sections():
    icon_size = config["systray"].getint(
        "icon_size", fallback=default_iconsize)
    widget_systray = widget.Systray(
        icon_size=icon_size,
    )
    widget_list.append(widget_systray)

if "wlan" in config.sections():
    interface = config["wlan"]["interface"]
    format = config["wlan"]["format"]
    disconnect_message = config["wlan"]["disconnect_message"]
    widget_wlan = widget.Wlan(
        interface=interface,
        format=format, 
        disconnect_message=disconnect_message,
    )
    widget_list.append(widget_wlan)

if "memory" in config.sections():
    format = config["memory"]["format"]
    widget_memory = widget.Memory(
        format=format,
    )
    widget_list.append(widget_memory)

if "cpu" in config.sections():
    format = config["cpu"]["format"]
    widget_cpu = widget.CPU(
        format=format,
    )
    widget_list.append(widget_cpu)

if "thermal_sensor" in config.sections():
    tag_sensor = config["thermal_sensor"]["tag_sensor"]
    fmt = config["thermal_sensor"]["fmt"]
    fmt = fmt.strip('"')
    fmt = fmt.strip("'")
    padding = config["thermal_sensor"].getint("padding")
    update_interval = config["thermal_sensor"].getint("update_interval")
    font = config["thermal_sensor"].get("font", fallback=default_font)
    fontsize = config["thermal_sensor"].getint(
        "fontsize", fallback=default_fontsize)
    foreground = config["thermal_sensor"].get(
        "foreground", fallback=default_foreground)
    widget_thermalsensor = widget.ThermalSensor(
        tag_sensor=tag_sensor,
        fmt=fmt,
        padding=padding,
        update_interval=update_interval,
        font=font,
        fontsize=fontsize,
        foreground=foreground,
    )
    widget_list.append(widget_thermalsensor)

if "volume" in config.sections():
    fmt = config["volume"]["fmt"]
    volume_app = config["volume"]["volume_app"]
    widget_volume = widget.Volume(
        fmt=fmt,
        volume_app=volume_app
    )
    widget_list.append(widget_volume)

if "battery" in config.sections():
    format = config["battery"]["format"]
    discharge_char = config["battery"]["discharge_char"]
    full_char = config["battery"]["full_char"]
    update_interval = config["battery"].getint("update_interval")
    widget_battery = widget.Battery(
        format=format,
        discharge_char=discharge_char,
        full_char=full_char,
        update_interval=update_interval,
    )
    widget_list.append(widget_battery)

if "clock" in config.sections():
    format = config["clock"]["format"]
    fontsize = config["clock"].getint(
        "fontsize", fallback=default_clock_fontsize)
    padding = config["clock"].getint("padding")
    widget_clock = widget.Clock(
        format=format,
        fontsize=fontsize,
        padding=padding,
    )
    widget_list.append(widget_clock)

screens = [
    Screen(bottom=bar.Bar(widget_list, size=bar_size, opacity=opacity)),
]
