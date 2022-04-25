|logo|

Linux Configs
=============

This repository contains config/dotfiles files for my Linux systems. This
contains all base files that are shared across different platforms or
computers. Strictly speaking, everything here should be compatible with
every Linux system so long as the dependency requirements are met.
So, this repo can be a good starting point for setting up or
restoring new Linux Machine.

Other configs that are platform/computer-dependent, e.g. mouse
acceleration settings, Wlan interface ID, thermal sensor ID, etc, are in
platform-dependent repository.
The idea is to use this repository as a submodule of the platform-dependent
repository. However, if one wishes to use this barebone repo directly, it is
also possible. If the same dotfile exists in both the main module and the
submodule, priority will be given to that in the main module.

Platform dependent repository:

|Base| |Arch-PC| |Arch-Blade| |Arch-AMD|

.. contents::
   :depth: 3


Getting Started
---------------

1. Install base dependencies (see below).
2. Create a repository using this as the template or other ones listed above
   if working with a new setup, or using one of them if reinstalling.

#. Clone and cd into the repo directory.

#. Link the config files using the install shell script.
   ``./install.sh``. This will create symbolic links for every dotfiles in the
   ``linux-configs/dotfiles`` to the home directory. And then, it will create
   symbolic links for every files/folders in ``linux-configs/dotfiles/.config``
   .

#. Restart or whatever to apply the new config files.

Note: ``install.sh`` does not overwrite existing files/folder. Observe the
output of ``./install.sh`` to see if there's any unsuccessful links.
If this is used as a submodule, there's no need to run this script. Running the
installation script in the main repository should suffice.
If the same dotfile exists in both the main module and the
submodule, priority will be given to that in the main module.
In this case, running ``./install.sh`` will output unsuccessful link when
linking those particular submodule dotfiles.

*If the dotfile is initially linked to a file in the submodule and you wish to
link it to that in the main module, remove the file first and then run*
``./install.sh`` *in the main module.*


Modifying Configuration Files
-----------------------------

This repo, ``linux-configs``, is used as submodules in other Linux
configuration repositories. Make sure any modification here will not cause
compatibility issues for other machines.


Dependencies
------------
Basic things such as Xorg is assumed and will not be specified here.
If dependencies requriements are not met, some dotfiles will still function.
To ensure full functionality, it is recommended to install all dependencies.

Required by my bashrc
^^^^^^^^^^^^^^^^^^^^^
- neofetch
- openssh (Optional)
- rdesktop (Optional)

Required by my xprofile
^^^^^^^^^^^^^^^^^^^^^^^
- Xorg
- imwheel
- ibus
- dropbox
- variety
- picom
- redshift

Required by my Qtile config
^^^^^^^^^^^^^^^^^^^^^^^^^^^
- Python
- qtile (There might be some other depencencies for widgets)
- alacritty
- shutter
- pavucontrol (Install alsa-utils and pulseaudio first)
- chromium
- atom
- rofi
- `rofi-themes <https://github.com/davatorium/rofi-themes>`__
- htop
- tty-clock


Required by my Rofi
^^^^^^^^^^^^^^^^^^^
- `Freemono font <https://fontmeme.com/fonts/freemono-font/>`__
  Download and extract the fonts. And then do
  ``cp *.ttf /usr/share/fonts/TTF/``

Miscellaneous
^^^^^^^^^^^^^
- mcmojave-cursors

Fonts
^^^^^
- `Freemono font <https://fontmeme.com/fonts/freemono-font/>`__
  Download and extract the fonts. And then do
  ``cp *.ttf /usr/share/fonts/TTF/``
- ttf-google-fonts-git
- ttf-joypixels
- adobe-source-han-sans-otc-fonts
- adobe-source-han-serif-otc-fonts
- nerd-fonts-dejavu-complete

Other useful information
^^^^^^^^^^^^^^^^^^^^^^^^
- `Git save credentials
  <https://www.tecmint.com/fix-git-user-credentials-for-https/>`__


.. |logo| image:: https://github.com/garrett/Tux/blob/main/tux.svg
    :alt: logo

..
  color: rgb, yellow, purple, cyan.

.. |Base| image:: https://img.shields.io/badge/branch-Base-red.svg
    :alt: Base
    :target: https://github.com/terrencetec/linux-configs

.. |Arch-PC| image:: https://img.shields.io/badge/branch-Arch--PC-green.svg
    :alt: Arch-PC
    :target: https://github.com/terrencetec/Arch-PC-configs

.. |Arch-Blade| image:: https://img.shields.io/badge/branch-Arch--Blade-blue.svg
    :alt: Arch-Blade
    :target: https://github.com/terrencetec/Arch-Blade-configs

.. |Arch-AMD| image:: https://img.shields.io/badge/branch-Arch--AMD-yellow.svg
    :alt: Arch-AMD
    :target: https://github.com/terrencetec/Arch-AMD-configs
