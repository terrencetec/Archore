import configparser
import os

from libqtile.config import Group


path_home = os.path.expanduser("~")
path_config = os.path.join(path_home, ".congig/qtile/workspaces.ini")
# For debugging:
if not os.path.exists(path_config):
    path_config = "workspaces.ini"

config = configparser.ConfigParser(allow_no_value=True)
config.optionxform = str
config.read(path_config)

groups = []

for workspace in config.sections():
    # The section name is the name of the workspace
    name = workspace
    spawn = config[workspace]["launch"]
    layout = config[workspace]["layout"]
    groups.append(Group(name=name, spawn=spawn, layout=layout))

# initial_group = Group(
#     name='1',
#     spawn=['{}'.format(terminal),
#            '{} -e htop'.format(terminal),
#            '{} -e tty-clock -s -c -t'.format(terminal),
#            ],
#     layout='monadtall',
# )

# groups = [initial_group] + [Group(i) for i in "234567"]
