"""Archore Qtile config

Do not modify this file directly for configuring your system.
Instead, modify config.ini, shortcuts.ini, and workspaces.ini.
"""
import configparser
import os

from libqtile import layout, hook
from libqtile.config import Click, Drag, Match
from libqtile.lazy import lazy

from floating_layout import floating_layout
from groups import groups
from keys import keys, mod
from layouts import layouts
from screens import screens, widget_defaults


path_home = os.path.expanduser('~')
path_config = os.path.join(path_home, ".config/qtile/config.ini")
# For debugging
if not os.path.exists(path_config):
    path_config = "config.ini"
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read(path_config)

auto_full_screen = config["qtile"].getboolean("auto_full_screen")
bring_front_click = config["qtile"].getboolean("bring_front_click")
cursor_warp = config["qtile"].getboolean("cursor_warp")
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
focus_on_window_activation = config["qtile"]["focus_on_window_activation"]
follow_mouse_focus = config["qtile"].getboolean("follow_mouse_focus")
reconfigure_screens = config["qtile"].getboolean("reconfigure_screens")
wmname = config["qtile"]["wmname"]
auto_minimize = config["qtile"].getboolean("auto_minimize")



# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# floating_layout = layout.Floating(
#     float_rules=[
#         # Run the utility of `xprop` to see the wm class and name of an X client.
#         *layout.Floating.default_float_rules,
#         Match(wm_class="confirmreset"),  # gitk
#         Match(wm_class="makebranch"),  # gitk
#         Match(wm_class="maketag"),  # gitk
#         Match(wm_class="ssh-askpass"),  # ssh-askpass
#         Match(title="branchdialog"),  # gitk
#         Match(title="pinentry"),  # GPG key password entry
#     ]
# )

wmname = "Qtile"

@hook.subscribe.startup_once
def autostart():
    pass
