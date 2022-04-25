import os
# import time
#
# from default_variables import cursor, terminal
# #
# # # time.sleep(0.1)
# # os.system('{} &'.format(terminal))
# # time.sleep(0.2)
# # os.system('{} -e htop &'.format(terminal))
# # time.sleep(0.2)
# # os.system('{} -e tty-clock -s -c -t &'.format(terminal))
# # # Flush qtile to get systray to properly space
# # time.sleep(0.4)
# # os.system('{} -e qtile-cmd -o group -f setlayout -a monadtall &'.format(terminal))
# #
#
# from libqtile.command_client import InteractiveCommandClient
#
# c = InteractiveCommandClient()
#
# windows_count = 0
#
# c.spawn('alacritty &')
# c.spawn('alacritty')
# c.spawn('alacritty')
# c.spawn('alacritty')
# c.spawn('alacritty')

home = os.path.expanduser('~')

override_path = home+'/.config/qtile_override'
if os.path.exists(override_path):
    import sys
    sys.path.append(override_path)

if os.path.exists(override_path+'/custom_autostart.py'):
    import custom_autostart
