import os

from libqtile.utils import guess_terminal


home = os.path.expanduser('~')

terminal = guess_terminal()

# modifier key. mod4 = super key, mod1 = alt key
mod = 'mod4'

# Wlan interface Intel Wi-Fi 6 AX200
wlan_interface = 'wlp3s0'

# tag_sensor discoverable by the ``sensor`` commend
tag_sensor = 'Package id 0'

# cursor
cursor = 'mcmojave-cursors'

# terminal override.
# terminal = 'alacritty'
terminal = 'urxvt'

# font
font = 'Freemono'
font_size = 18

# bar and stuff
bar_size = 32
trayicon_multiplier = 3/4
clock_font_multiplier = 1/2
bar_opacity = 1

# color
terminal_green = '#00ff66'

# MonadTall configs
layout_margin = 16
layout_ratio = 0.7

# Battery Widget
battery_widget = False

# Icon path
if os.path.exists(home+'/.config/qtile_override/icon.png'):
    icon_path = home+'/.config/qtile_override/icon.png'
else:
    icon_path = home+'/.config/qtile/icon.png'

override_path = home+'/.config/qtile_override'
if os.path.exists(override_path):
    import sys
    sys.path.append(override_path)

if os.path.exists(override_path+'/custom_variables.py'):
    from custom_variables import *
