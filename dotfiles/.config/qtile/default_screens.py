from libqtile import bar, widget, qtile
from libqtile.config import Screen
from libqtile.lazy import lazy

from default_variables import (
    home, wlan_interface, tag_sensor, font, font_size, bar_size,
    trayicon_multiplier, clock_font_multiplier, terminal_green,
    battery_widget, icon_path, bar_opacity
)


widget_defaults = dict(
    font=font,
    fontsize=font_size,
    foreground=terminal_green
)
default_font = font
default_fontsize = font_size
default_clock_fontsize = int(font_size/2)
default_foreground = terminal_green
default_icon_path = home+"/.config/qtile/icon.png"
extension_defaults = widget_defaults.copy()

def rofi_exit():
    qtile.cmd_spawn(home+"/.config/rofi/rofi-exit.sh")

import configparser
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read(home+"/.config/qtile/widget_config.ini")

widget_list = []

if "image" in config.sections():
    margin = config["image"].getint("margin")
    icon_path = config["image"].get("icon_path", fallback=default_icon_path)
    widget_image = widget.Image(
        margin=margin, filename=icon_path,
        mouse_callbacks={"Button1": rofi_exit})
    widget_list.append(widget_image)

if "group_box" in config.sections():
    active_color = config["group_box"]["active_color"]
    block_highlight_text_color = (
        config["group_box"]["block_highlight_text_color"])
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
    icon_size = config["systray"].getint("icon_size")
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
    padding = config["thermal_sensor"].getint("padding")
    update_interval = config["thermal_sensor"].getint("update_interval")
    font = config["thermal_sensor"].get("font", fallback=default_font)
    fontsize = config["thermal_sensor"].getint(
        "fontsize", fallback=default_fontsize)
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

# icon_config = {
#     'margin': 3,
#     'filename': icon_path,
#     'mouse_callbacks': {
#         'Button1':rofi_exit,},
# }

# task_list_config = {
#     'border': '#666666',
#     'border_width': 1,
#     'font': font,
#     'margin': 3,
#     'max_title_width': 250,
#     'padding': 4,
#     'rounded': False,
#     'unfocused_border':'#333333',
# }

# widget_list = [
#     widget.Image(**icon_config),
#     widget.GroupBox(
#         active='AAAAAA',
#         block_highlight_text_color=terminal_green,
#         borderwidth=3,
#         highlight_method='line'),
#     widget.TaskList(**task_list_config),
#     widget.CurrentLayout(fmt='{0:>9s}'),
#     widget.Prompt(),
#     widget.Systray(icon_size=int(bar_size*trayicon_multiplier)),
#     widget.Wlan(
#         interface=wlan_interface,
#         format='W:{percent:2.0%}',
#         disconnected_message='W:DC!',
#     ),
#     widget.Memory(
#         # format='M:{MemUsed}M/{MemTotal}M'
#         format='M:{MemPercent}%'
#     ),
#     widget.CPU(
#         format='C:{load_percent:4.1f}%',
#     ),
#     widget.ThermalSensor(
#         tag_sensor=tag_sensor,
#         fmt='{} ',
#         padding=3,
#         update_interval=1,
#         **widget_defaults,),
#     widget.Volume(
#         fmt='V:{:>4}',
#         volume_app='pavucontrol'
#     ),
#     widget.Clock(
#         format='%I:%M:%S %p\n%Y-%m-%d %a',
#         fontsize=int(bar_size*clock_font_multiplier),
#         padding=8)
# ]

# if battery_widget:
#     widget_list.insert(-1,
#         widget.Battery(format='B:{char} {percent:2.0%} {hour:d}:{min:02d}',
#                        discharge_char='v',
#                        full_char="=",
#                        update_interval=5)
#     )

screens = [
    Screen(bottom=bar.Bar(widget_list, size=bar_size, opacity=bar_opacity)),
]
