import os
import configparser

from libqtile.lazy import lazy
from libqtile.config import Key


path_home = os.path.expanduser("~")
path_keys_config = os.path.join(path_home, ".config/qtile/shortcuts.ini")
path_workspaces_config = os.path.join(
    path_home, ".config/qtile/workspaces.ini")
# For debugging
if not os.path.exists(path_keys_config):
    path_keys_config = "shortcuts.ini"
if not os.path.exists(path_workspaces_config):
    path_workspaces_config = "workspaces.ini"

keys_config = configparser.ConfigParser(allow_no_value=True)
keys_config.optionxform = str
keys_config.read(path_keys_config)
workspaces_config = configparser.ConfigParser(allow_no_value=True)
workspaces_config.optionxform = str
workspaces_config.read(path_workspaces_config)

list_of_modifiers = [
    "mod1", "mod2", "mod3", "mod4", "mod5", "control", "shift", "lock"
]


def decipher_shortcut(shortcut, delimiter="+", mod="mod4", **kwargs):
    """Convert shortcuts from configuration files to modifers and keys.

    Parameters
    ----------
    shortcut : str
        A string of shortcuts comprise of a list of modifiers
        and keys separated by the ``delimiter`` sign.
        Spaces are removed automatically
        Example: mod + 4 and mod + shift+4.
        Note that there can only be one key.
        If multiple keys are detected, e.g. mod + 4 + 5, only the last
        one will be taken.
    delimiter : str, optional
        Delimited separating different modifiers/keys.
        Defaults to "+".
    mod : str, optional
        Replace "mod" in the string by this string.
        Defaults to "mod4".
    **kwargs :
        Keyword arguments eater.

    Returns
    -------
    modifiers : list of str
        A list of modifiers.
        Modifiers are ``mod1``-``mod5``, ``control``, ``shift``, ``lock``.
    key : str
        The key.
    """
    shortcut = shortcut.replace(" ", "")
    list_keys = shortcut.split(delimiter)
    # Replace the "mod" string with specified mod modifier.
    for i, button in enumerate(list_keys):
        if button == "mod":
            list_keys[i] = mod
    modifiers = []
    keys = [""]
    for button in list_keys:
        if button in list_of_modifiers:
            modifiers.append(button)
        else:
            keys.append(button)
    key = keys[-1]
    
    return modifiers, key


def add_shortcut(shortcuts, command, keys=None, desc="", **kwargs):
    """Add shortcut
    
    Parameters
    ----------
    shortcuts : str
        A string of shortcuts comprise of a list of modifiers
        and keys separated by the ``delimiter`` sign
        Spaces are removed automatically
        Example: mod + 4 and mod + shift+4.
        Note that there can only be one key.
        If multiple keys are detected, e.g. mod + 4 + 5, only the last
        one will be taken.
        In addition, multiple shortcuts can be specified by separating
        them with an "or" string, e.g. mod+4 or mod + 5.
    command : libqtile.lazy.LazyCall
        The Qtile command to be excuted.
    keys : list of libqtile.config.Key, optional
        The list of libqtile.config.Key to be appended to.
        Defaults to [].
    desc : str, optional
        The description of this shortcut.
        Defaults to "".
    **kwargs :
        Keyword arguments passed to decipher_shortcut().

    Returns
    -------
    List of libqtile.config.Key
        The list of shortcuts.
    """
    if keys is None:
        keys = []
    # Handle multiple shortcut.
    for shortcut in shortcuts.split("or"):
        modifiers, key = decipher_shortcut(shortcut, **kwargs)
        print(modifiers, key, desc)
        keys.append(
            Key(modifiers, key, command, desc=desc)
        )
    return keys


keys = []

# Add shortcuts for switch workspaces, etc.
mod = keys_config["modifier"]["mod"]
mod_toscreen = keys_config["workspace modifiers"]["toscreen"]
mod_togroup = keys_config["workspace modifiers"]["togroup"]

workspaces = workspaces_config.sections()

for workspace in workspaces:
    key = workspaces_config[workspace]["key"]
    shortcuts = f"{mod_toscreen} + {key}"
    command = lazy.group[workspace].toscreen()
    desc = f"Move to workspace {workspace}"
    keys = add_shortcut(
        shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)
    shortcuts = f"{mod_togroup} + {key}"
    command = lazy.window.togroup(workspace, switch_group=True)
    desc = f"Move focused window and switch to workspace {workspace}"
    keys = add_shortcut(
        shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

# Layout control
shortcuts = keys_config["layout"]["up"]
command = lazy.layout.up()
desc = "Focus window above"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["down"]
command = lazy.layout.down()
desc = "Focus window below"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["left"]
command = lazy.layout.left()
desc = "Focus window below"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["right"]
command = lazy.layout.right()
desc = "Focus window below"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["next"]
command = lazy.layout.next()
desc = "Focus next window"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["shuffle up"]
command = lazy.layout.shuffle_up()
desc = "Move window above"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["shuffle down"]
command = lazy.layout.shuffle_down()
desc = "Move window below"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["shuffle left"]
command = lazy.layout.swap_left()
desc = "Move window below"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["shuffle right"]
command = lazy.layout.swap_right()
desc = "Move window below"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["grow"]
command = lazy.layout.grow()
desc = "Grow focus window"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["shrink"]
command = lazy.layout.shrink()
desc = "Shrink window below"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["normalize"]
command = lazy.layout.normalize()
desc = "Normalize window size"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["flip"]
command = lazy.layout.flip()
desc = "Flip layout"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["maximize"]
command = lazy.layout.maximize()
desc = "Maximize layout"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["next layout"]
command = lazy.next_layout()
desc = "Next layout"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["layout"]["prev layout"]
command = lazy.prev_layout()
desc = "Previous layout"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)


# Windows control
shortcuts = keys_config["window"]["toggle floating"]
command = lazy.window.toggle_floating()
desc = "Toggle floating"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["window"]["toggle minimize"]
command = lazy.window.toggle_minimize()
desc = "Toggle minimize"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["window"]["kill"]
command = lazy.window.kill()
desc = "Kill focused window"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

# Screen control
shortcuts = keys_config["screen"]["next group"]
command = lazy.screen.next_group()
desc = "Move to next workspace"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["screen"]["prev group"]
command = lazy.screen.prev_group()
desc = "Move to previous workspace"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

# Qtile control
shortcuts = keys_config["qtile"]["restart"]
command = lazy.restart()
desc = "Restart Qtile"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

shortcuts = keys_config["qtile"]["spawncmd"]
command = lazy.spawncmd()
desc = "Spawn a command using a prompt widget"
keys = add_shortcut(
    shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)

# Custom launch commands
command_key_pairs = dict(keys_config["launch"].items())
for launch_command in command_key_pairs.keys():
    shortcuts = command_key_pairs[launch_command]
    if "~" in launch_command:
        home = os.path.expanduser("~")
        launch_command = launch_command.replace("~", home)
    desc = launch_command
    command = lazy.spawn(launch_command)
    keys = add_shortcut(
        shortcuts=shortcuts, command=command, desc=desc, keys=keys, mod=mod)
