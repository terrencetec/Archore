# from typing import List  # noqa: F401
from libqtile.lazy import lazy
from libqtile.config import Group

from default_variables import terminal
from default_layouts import layouts


initial_group = Group(
    name='1',
    spawn=['{}'.format(terminal),
           '{} -e htop'.format(terminal),
           '{} -e tty-clock -s -c -t'.format(terminal),
           ],
    layout='monadtall',
)

groups = [initial_group] + [Group(i) for i in "234567"]
