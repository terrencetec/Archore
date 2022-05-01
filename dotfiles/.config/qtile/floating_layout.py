"""Floating layout config

Do not edit this file directly.
Instead, edit floating_layout.ini.
"""
import configparser
import os

from libqtile import layout
from libqtile.config import Match


path_home = os.path.expanduser('~')
path_config = os.path.join(path_home, ".config/qtile/floating_layout.ini")
# For debugging
if not os.path.exists(path_config):
    path_config = "floating_layout.ini"
config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read(path_config)

use_default_float_rules = config["default"].getboolean(
    "use_default_float_rules")
if use_default_float_rules:
    float_rules = [*layout.Floating.default_float_rules]
else:
    float_rules = []

for title in list(config["title"].keys()):
    float_rules.append(
        Match(title=title)
    )

for wm_class in list(config["wm_class"].keys()):
    float_rules.append(
        Match(wm_class=wm_class)
    )

for role in list(config["role"].keys()):
    float_rules.append(
        Match(role=role)
    )

for wm_type in list(config["wm_type"].keys()):
    float_rules.append(
        Match(wm_type=wm_type)
    )

for wm_instance_class in list(config["wm_instance_class"].keys()):
    float_rules.append(
        Match(wm_instance_class=wm_instance_class)
    )

for net_wm_pid in list(config["net_wm_pid"].keys()):
    float_rules.append(
        Match(net_wm_pid=net_wm_pid)
    )

floating_layout = layout.Floating(float_rules=float_rules)