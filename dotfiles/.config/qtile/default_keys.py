
import os

from libqtile.lazy import lazy
from libqtile.config import Key

from default_variables import home, mod, terminal
from default_groups import groups


keys = [
    # Switch between windows (MonadTall)
    Key([mod], "Up", lazy.layout.up(), desc="Focus window above"),
    Key([mod], "Down", lazy.layout.down(), desc="Focus window below"),
    Key([mod], "Left", lazy.layout.left(), desc="Focus window left"),
    Key([mod], "Right", lazy.layout.right(), desc="Focus window right"),

    # Move windows (MonadTall)
    Key([mod, "shift"], "Up",
        lazy.layout.shuffle_up(),
        desc="Move windows up"),
    Key([mod, "shift"], "Down",
        lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "Left",
        lazy.layout.swap_left(),
        desc="Move window left"),
    Key([mod, "shift"], "Right",
        lazy.layout.swap_right(),
        desc="Move window right"),

    # Grow/Shrink main pane (MonadTall)
    Key([mod, "control"], "equal",
        lazy.layout.grow(),
        desc="Grow focus window"),
    Key([mod, "control"], "minus",
        lazy.layout.shrink(),
        desc="Shrink focus window"),

    # Windows manipulation. (Mond)
    Key([mod, "control"], "n",
        lazy.layout.normalize(),
        desc="Normalize window size"),
    Key([mod, "control"], "f",
        lazy.layout.flip(),
        desc="Flip layout"),
    Key([mod, "control"], "m",
        lazy.layout.maximize(),
        desc="Maximize layout"),

    # Toggle between different layouts as defined below
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle float"),
    Key([mod], "q", lazy.window.toggle_minimize(), desc="Toggle minimize"),

    # Key([mod, 'control'], "Tab", lazy.next_layout()),
    Key([mod], 'space', lazy.next_layout(), desc="Next layout"),
    Key([mod, "control"], "Down", lazy.next_layout(), desc="Next layout"),
    Key([mod, "control"], "Up", lazy.prev_layout(), desc="Previous layout"),
    Key([mod], "Tab", lazy.screen.next_group(), desc="Next group"),
    Key([mod, 'shift'], "Tab",
        lazy.screen.prev_group(),
        desc="Previous group"),
    Key([mod, "control"], "Right",
        lazy.screen.next_group(),
        desc="Next group"),
    Key([mod, "control"], "Left",
        lazy.screen.prev_group(),
        desc="Next group"),

    # May use rofi instead. See below.
    Key(['mod1'], "Tab", lazy.layout.next(), desc="Switch focus"),
    # Directly Alt-Tab to switch windows instead
    # Key(['mod1'], 'Tab', lazy.spawn('rofi -show window -theme \
    #                                 ~/.local/share/rofi/themes/slate.rasi\
    #                                 -font "Freemono 16" -lines 10')),
    Key(['mod1'], "F4", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "F4", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Custom Shortcuts
    Key([mod, "shift"], "s", lazy.spawn('shutter -s'), desc="Launch shutter"),
    Key(["control", "mod1"], "t", lazy.spawn(terminal),
        desc="Launch terminal"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "p", lazy.spawn('pavucontrol'), desc="Launch pavucontrol"),
    Key([mod], "g", lazy.spawn('google-chrome-stable'),
        desc="Launch google-chrome-stable"),
    Key([mod], "i",
        lazy.spawn("google-chrome-stable --incognito"),
        desc="Launch google-chrome-stable incognito"),
    # Key([mod], "g", lazy.spawn('chromium'), desc="Launch chromium"),
    # Key([mod], "i",
    #     lazy.spawn("chromium --incognito"),
    #     desc="Launch chromium incognito"),
    Key([mod], "a", lazy.spawn("atom")),
    # Key([mod], 'a', launch_editor()),
    Key([mod], "d",
        lazy.spawn("rofi -show drun \
                   -theme \
                   ~/.config/rofi/drun_theme.rasi \
                   -font 'monospace 10' -l 100 -width 30"),
        desc="Launch rofi drun"),
    Key([mod, "shift"], "Escape",
        lazy.spawn(home+"/.config/rofi/rofi-exit.sh"),
        desc="Launch rofi exit"),
    
    # Fn controls
    ## Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5"),
        desc="Brightness up"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5"),
        desc="Brightness down"),
    ## Audio
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"),
        desc="Audio mute"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 2%-"),
        desc="Audio lower volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 2%+"),
        desc="Audio raise volume"),
]

for group in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], group.name, lazy.group[group.name].toscreen(),
            desc="Switch to group {}".format(group.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], group.name,
            lazy.window.togroup(group.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(group.name)),
    ])
