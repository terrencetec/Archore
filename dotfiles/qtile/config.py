# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import time

from libqtile import layout, hook
from libqtile.config import Click, Drag, Match
from libqtile.lazy import lazy

from default_variables import mod, terminal
from default_keys import keys
from default_layouts import layouts
from default_groups import groups
from default_screens import screens, widget_defaults


# Custom things.
home = os.path.expanduser('~')
override_path = home+'/.config/qtile_override'
if os.path.exists(override_path):
    import sys
    sys.path.append(override_path)

if os.path.exists(override_path+'/custom_groups.py'):
    from custom_groups import groups_override, groups_append
    if groups_override is not None:
        groups = groups_override
    if groups_append is not None:
        groups += groups_append

if os.path.exists(override_path+'/custom_keys.py'):
    from custom_keys import keys_override, keys_append
    if keys_override is not None:
        keys = keys_override
    if keys_append is not None:
        keys += keys_append
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='ssh-askpass'),  # ssh-askpass

    Match(wm_class='shutter'),
    Match(wm_class='lxappearance'),
    Match(wm_class='pavucontrol'),
    Match(wm_class='ibus-setup'),
    Match(wm_class='zoom'),
    Match(wm_class='qbittorrent'),
    Match(role='pop-up'),
])
auto_fullscreen = True
focus_on_window_activation = "smart"

wmname = "Qtile"

@hook.subscribe.startup_once
def autostart():
    import default_autostart
