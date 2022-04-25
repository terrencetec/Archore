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

extension_defaults = widget_defaults.copy()

def rofi_exit():
    qtile.cmd_spawn(home+"/.config/rofi/rofi-exit.sh")

icon_config = {
    'margin': 3,
    'filename': icon_path,
    'mouse_callbacks': {
        'Button1':rofi_exit,},
}

task_list_config = {
    'border': '#666666',
    'border_width': 1,
    'font': font,
    'margin': 3,
    'max_title_width': 250,
    'padding': 4,
    'rounded': False,
    'unfocused_border':'#333333',
}

widget_list = [
    widget.Image(**icon_config),
    widget.GroupBox(
        active='AAAAAA',
        block_highlight_text_color=terminal_green,
        borderwidth=3,
        highlight_method='line'),
    widget.TaskList(**task_list_config),
    widget.CurrentLayout(fmt='{0:>9s}'),
    widget.Prompt(),
    widget.Systray(icon_size=int(bar_size*trayicon_multiplier)),
    widget.Wlan(
        interface=wlan_interface,
        format='W:{percent:2.0%}',
        disconnected_message='W:DC!',
    ),
    widget.Memory(
        # format='M:{MemUsed}M/{MemTotal}M'
        format='M:{MemPercent}%'
    ),
    widget.CPU(
        format='C:{load_percent:4.1f}%',
    ),
    widget.ThermalSensor(
        tag_sensor=tag_sensor,
        fmt='{} ',
        padding=3,
        update_interval=1,
        **widget_defaults,),
    widget.Volume(
        fmt='V:{:>4}',
        volume_app='pavucontrol'
    ),
    widget.Clock(
        format='%I:%M:%S %p\n%Y-%m-%d %a',
        fontsize=int(bar_size*clock_font_multiplier),
        padding=8)
]

if battery_widget:
    widget_list.insert(-1,
        widget.Battery(format='B:{char} {percent:2.0%} {hour:d}:{min:02d}',
                       discharge_char='v',
                       full_char="=",
                       update_interval=5)
    )

screens = [
    Screen(bottom=bar.Bar(widget_list, size=bar_size, opacity=bar_opacity)),
]
