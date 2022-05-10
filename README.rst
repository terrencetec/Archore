Archore
=======
Core scripts, templates, configuration files, and instructions for setting up my Arch Linux.

.. contents::
   :depth: 3 
   
Installation
============
| Follow the instructions below.
| When in doubt, consult `installation guide <https://wiki.archlinux.org/title/Installation_guide>`_ in ArchWiki.
| Boot into the installation live media and do the followings in the exact order.
| To write the live image to a USB drive, type

.. code-block:: bash

   dd if=/path/to/live/image.iso of=/dev/usb_device status=progress

Remember to use ``lsblk`` to check the USB drive's assigned block device, e.g. ``/dev/sda``.

Connect to the internet
-----------------------
Use ``iwctl``.

Type ``iwctl`` to enter an interactive prompt.

.. code-block::

   [iwd]#
   
Then, type the following commands to connect to your WIFI.

.. code-block::

   [iwd]# device list

.. code-block::

   [iwd]# station device scan

where ``device`` is your device.

.. code-block::

   [iwd]# station device get-networks

.. code-block::

   [iwd]# station device connect SSID
   
where ``SSID`` is your WIFI SSID.

Type ``exit`` to exit the prompt.

After that, confirm connection is established by

.. code-block:: bash

   ping google.com


Partition
---------
| Use ``lsblk`` or ``fdisk -l`` to identify the disk that you want you partition.
| Use ``cfdisk`` utility instead of `fdisk`.

Operating system drive
^^^^^^^^^^^^^^^^^^^^^^
| Type ``cfdisk /dev/*disk*`` in the Arch Linux live environment.
| After that, select ``gpt`` lable type.
| ``cfdisk`` is a self explanatory utility.
| Format the disk as with the following partitions (with the exact order, but size is flexible.):

+-----------+-------------------+----------------------------+
|mount point|partition type     |size                        |
+===========+===================+============================+
|/efi       |EFI system         |at least 300M (I used 512Mb)|
+-----------+-------------------+----------------------------+
|[SWAP]     |Linux swap         |The size of physical ram    |
+-----------+-------------------+----------------------------+
|/          |Linux root (x86-64)|Remainder                   |
+-----------+-------------------+----------------------------+

Storage drive
^^^^^^^^^^^^^
+-------------+-----------------------+----------------------------+
|mount point  |partition type         |size                        |
+=============+=======================+============================+
|/storage     |Linux filesystem       |Remainder                   |
+-------------+-----------------------+----------------------------+
|/storage2    |Microsoft storage space|Remainder                   |
+-------------+-----------------------+----------------------------+

Formatting
----------
For root partition and storage partitions (Linux exclusive storage devices)

.. code-block:: bash

   mkfs.ext4 /dev/partition

For storage partitions shared with Windows

.. code-block:: bash

   mkfs.ntfs /dev/partition

For swap partition

.. code-block:: bash

   mkswap /dev/swap_partition

For EFI partition

.. code-block:: bash

  mkfs.fat -F 32 /dev/efi_partition
  
Mounting the partitions
-----------------------
Mount root partition

.. code-block:: bash
   
   mount /dev/root_partition /mnt
   
Mount EFI partition

.. code-block:: bash

   mount --mkdir /dev/efi_partition /mnt/efi

Mount other partitions

.. code-block:: bash

   mount --mkdir /dev/other_partitions /mnt/other_mount_points

For addition storages, change the group of the directory and permission

.. code-block:: bash

   chmod 775 /path/to/storage
   chown root:storage /path/to/storage

Enable swap

.. code-block:: bash

   swapon /dev/swap_partition
   
   
Update mirror list
------------------
Use reflector

.. code-block:: bash

   reflector --country country --protocol https --sort score --save /etc/pacman.d/mirrorlist
etc\pacman.d\mirrorlist

| Replace ``country`` with a comma separated list, e.g. ``Hong\ Kong,Japan``.
| To get a list of countries, run

.. code-block:: bash

   reflector --list-countries | less


Install essential packages
--------------------------
Use pacstrap

.. code-block:: bash

   pacsctrap /mnt base base-devel linux linux-headers linux-firmware linux-lts linux-lts-headers
   
``linux-lts`` and ``linux-lts-headers`` are optional.

| Append the following list of packages as appropriate.
| **Only install packages that are required for the installation process.**
| Other user packages can be installed after the installation.

.. code-block:: bash
   
   gvim git man-db man-pages texinfo ntfs-3g networkmanager sudo openssh
   
| Note, ``gvim`` contains the ``vim`` with ``+clipboard`` capability.
| If ``+clipboard`` capability is not required, then replace ``gvim`` with ``vim`` instead.
   
Configure the system
--------------------
Fstab
^^^^^

.. code-block:: bash

   genfstab -U /mnt >> /mnt/etc/fstab
   
Check result in /mnt/etc/fstab in case of error.

Chroot
^^^^^^
.. code-block:: bash

   arch-chroot /mnt
   
Time zone
^^^^^^^^^
.. code-block:: bash
   
   ln -sf /usr/share/zoneinfo/Region/City /etc/localtime
   
Run ``hwclock`` to generate ``/etc/adjtime``

.. code-block:: bash

   hwclock --systohc

Sync time.

.. code-block:: bash

   timdatectl set-ntp 1

Localization
^^^^^^^^^^^^
Edit ``/etc/locale.gen`` and uncomment ``en_US.UTF-8 UTF-8`` and other required locales.

.. code-block:: bash

   # /etc/locale.gen
   ...
   en_US.UTF-8 UTF-8
   ...
   zh_HK.UTF-8 UTF-8
   ...

After that, run

.. code-block:: bash

   locale-gen

Create ``/etc/locale.conf`` and set the ``LANG`` variable

.. code-block:: bash

   # /etc/locale.conf
   LANG=en_US.UTF-8

Network configuration
^^^^^^^^^^^^^^^^^^^^^
Creat ``/etc/hostname``

.. code-block:: bash

   # /etc/hostname
   myhostname
   
| I use the following convention for ``myhostname``: *name-OS*, e.g. ``Terrence-Linux``.
| If necessary, add suffix to avoid ambiguity, e.g. ``Terrence-Linux-1`` or ``Terrence-Linux-5900X``.

Root password
^^^^^^^^^^^^^
Type

.. code-block:: bash

   passwd
   
and set the root password

Microcode
^^^^^^^^^
Install ``intel-ucode`` for Intel processors or ``amd-ucode`` for AMD processors:

.. code-block:: bash

   pacman -Syu intel-ucode

or

.. code-block:: bash

   pacman -Syu amd-ucode

Boot loader
^^^^^^^^^^^
Install ``grub`` and ``efibootmgr`` (and ``os-prober`` if dual boot)

.. code-block:: bash

   pacman -Syu grub efibootmgr os-prober

Install boot loader

.. code-block:: bash

   grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB
   
Edit the following in ``/etc/default/grub``

.. code-block:: bash

   # /etc/default/grub
   ...
   GRUB_DEFAULT=saved
   ...
   GRUB_SAVEDEFAULT=true
   ...
   GRUB_DISABLE_SUBMENU=y
   ...
   # If dual-boot,
   GRUB_DISABLE_OS_PROBER=false

For dual-booting, remember to mount other OS's efi partition and use ``os-prober``.

After making changes in ``/etc/default/grub``, remember to generate ``/boot/grub/grub.cfg`` by typing

.. code-block:: bash

   grub-mkconfig -o /boot/grub/grub.cfg

Post installation
=================
Feel free to reboot and remove the installation media. Or, simply continue.

Create system user
------------------
| Create user and change password using ``useradd`` and ``passwd``.
| Replace ``groups`` with ``wheel,audio,video,disk,storage,input`` and additional groups as needed.

.. code-block:: bash

   useradd -m -G groups terrencetec
   passwd terrencetec

sudo
^^^^
Type

.. code-block:: bash

   visudo
   
to edit the sudoer file.

Uncomment the following line (line 82)

.. code-block:: bash

   %wheel ALL=(ALL) ALL

Change user
-----------
Switch to the user.

.. code-block:: bash

   su terrencetec

Switch to the user home directory

.. code-block:: bash

   cd ~

Install Paru
------------
.. code-block::

   git clone https://aur.archlinux.org/paru.git
   cd paru
   makepkg -si


Clone this repository
---------------------
Go back to home directory before cloning, i.e. don't clone this into the ``paru`` directory.

.. code-block:: bash

   git clone https://github.com/terrencetec/Archore.git
   
Or, use ssh if you are me. In this case, generate ssh-key and upload it to GitHub prior to this.

.. code-block:: bash

   ssh-keygen -t ed25519 -C "terrencetec@gmail.com"

| And find the public key in where it is generated and somehow copy the thing to GitHub.
| Then, clone with ssh   

.. code-block:: bash

   git clone git@github.com:terrencetec/Archore.git

(Optional) Enable ``pacman`` parallel downloads and eyecandy
------------------------------------------------------------
Edit ``/etc/pacman.conf`` and uncomment/add the following lines.

.. code-block:: bash

   # /etc/pacman.conf
   ...
   ParallelDownloads = 5
   ILoveCandy
   ...

Enable ``multilib``
^^^^^^^^^^^^^^^^^^^
| This enables 32-bit stuff, ``steam``, ``lib32-*``, etc...
| If this is not enabled, packages containing ``lib32-`` prefix cannot be found when attempting to install them.
| Edit ``/etc/pacman.conf``.
| Uncomment the following lines (around line 94-95)

.. code-block:: bash
   
      [multilib]
      Include = /etc/pacman.d/mirrorlist

(Look ahead) Install all packages below
---------------------------------------
All core packages are listed below, i.e. ``pkglist-core.txt``,
``pkglist-core-applications.txt``, ``pkglist-core-fonts.txt``,
and ``pkglist-core-eyecandy.txt`` are merged to ``pkglist-core-merged.txt``.

To install all core packages, type

.. code-block:: bash

   paru -Syu - < pkglist-core-merged.txt

Then, install optional packages:

.. code-block:: bash

   paru -Syu - < pkglist-optional.txt

Install core packages
---------------------
| The core packages of my Linux system is listed in ``pkglist-core.txt``.
| It contains
.. code-block:: bash

   xorg  # The display server.
   xdg-user-dirs  # Create folders such as Downloads, Pictures, in home directory.
   qtile  # My favorite window-tiling manager
   python-pip  # Python package manager.
   wireless_tools  # For my qtile's wlan widget.
   ly  # Display manager, i.e. login screen.
   slock  # Display locker
   xss-lock  # X session locker 
   rxvt-unicode  # My favorite terminal emulator
   rxvt-unicode-terminfo
   urxvt-perls
   urxvt-resize-font-git
   rofi  # My favorite program launcher
   alsa-utils  # Audio stuff.
   pulseaudio  # Audio stuff.
   pavucontrol # Audio stuff

Install them using ``paru``.

.. code-block:: bash
   
   cd Archore
   paru -Syu - < pkglist-core.txt

Alternatively, add the ``--needed`` tag to avoid reinstalling packages

.. code-block:: bash

   paru -Syu --needed < pkglist-core.txt

Python dependencies for my qtile configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Optionally, install required Python packages for qtile.

.. code-block::

   pip install iwlib psutil screeninfo

(Optional) Core applications, fonts, and eye candy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Install applications listed in ``pkglist-core-applications.txt``, ``pkglist-core-fonts``, and
``pkglist-core-eyecandy.txt``.

.. code-block:: bash

   paru -Syu - < pkglist-core-applications.txt

.. code-block:: bash
   
   paru -Syu - < pkglist-core-fonts.txt
   
.. code-block:: bash

   paru -Syu - < pkglist-core-eyecandy.txt

The ``pkglist-core-applications.txt`` list contains

.. code-block:: bash

   imwheel
   google-chrome
   shutter
   ibus
   ibus-table-chinese
   dropbox
   dropbox-cli
   signal-desktop
   lm-sensors

The ``pkglist-core-fonts.txt`` list containts

.. code-block:: bash

   nerd-fonts-dejavu-complete
   adobe-source-han-sans-otc-fonts
   adobe-source-han-serif-otc-fonts
   tty-joypixels
   
And, the ``pkglist-core-eyecandy.txt`` list contains

.. code-block:: bash

   neofetch
   variety
   picom
   redshift
   htop
   tty-clock-git
   mcmojave-cursors
   xcb-util-cursor  # Required by Qtile

The system doesn't require these applications and utilities to work.
However, some `configuration files <https://github.com/terrencetec/Archore/blob/master/README.rst#configurations-for-core-programs>`_
of the core programs were built around these applications and utilities.
So, it's best if these applications are installed as well.

Remember to setup ``ibus``, ``dropbox`` and ``variety``.
For ``variety``, I use my Arch wallpapers in ``Dropbox/wallpapers/``.

Dropbox GPG key
^^^^^^^^^^^^^^^
**NOTE**, before installing dropbox, you might have to import gpg key.
Type:

.. code-block:: bash

   gpg --recv-keys --keyserver hkp://pgp.mit.edu:80 FC918B335044912E

or simply run ``./import-dropbox-gpg-key.sh``

Ibus setup
^^^^^^^^^^
I use Alt+Shift_L as my shortcut for switching input method.
To set this, type ``ibus-setup`` in a terminal.
Click the three dots on the right.
In the "Key code" box, type "Shift_L".
And select "Alt" as the modifier.
Press "add".

Select the Input Method tab.
Click "add".
Select Chinese and find "Quick Classic".
Click "Preference".
For Chinese mode, select "All Chinese characters".
For page size, select "9".
Select the Details tab.
Untick "Auto select"

Variety
^^^^^^^
Click the Variety tray icon and click preference.
Untick "Start Variety when the computer starts".
Change wallpaper every "30 minutes".
Tick "Change wallpaper on start".
Click "Add..." on the right.
Add ``/home/username/Dropbox/wallpapers/``.
Untick other image sources and tick the dropbox/wallpapers/ source.

Graphics card driver
^^^^^^^^^^^^^^^^^^^^

| In addition, install graphics card driver.
| For AMD GPUs:

.. code-block:: bash

   paru mesa xf86-video-amdgpu vulkan-radeon libva-mesa-driver lib32-mesa lib32-vulkan-radeon lib32-libva-mesa-driver

For Nvidia GPUs:

.. code-block::

   paru nvidia lib32-nvidia-utils

For LTS kernels, also install ``nvidia-lts``

.. code-block::

   paru nvidia-lts

Or use the package lists in the repository.

.. code-block::

   paru -S - < pkglist-amdgpu.txt

.. code-block::

   paru -S - < pkglist-nvidia.txt

Enable core services
--------------------
Use ``systemctl``

Network
^^^^^^^
.. code-block::

   sudo systemctl enable NetworkManager.service

Display manager
^^^^^^^^^^^^^^^
.. code-block:: bash

   sudo systemctl enable ly.service

Configurations for core programs
-------------------------------
The ``dotfiles`` directory contains

- ``.bashrc`` Default bash initiation script
- ``.bashrc.custom`` User-defined bash initiation script.
- ``.xprofile`` Default autostart script. 
- ``.xprofile.custom`` User-defined autostart script.
- ``.Xdefaults`` Configurations for urxvt and others.
- ``.Xresources`` Other configurations, cursors, etc...
- ``.vimrc`` Configuration for vim. Remember to install extensions.
- ``imwheelrc`` IMWheel config. Install ``imwheel`` for this to take effect.
- ``.config/`` Configuration directory containing.
   - ``gtk-3.0/`` Constains cursor theme settings
   - ``picom/`` Picom configuration directory. Install ``picom`` for this to take effect.
   - ``qtile/`` Qtile configuration directory.
   - ``rofi/`` Rofi configuration directory.
   - ``chrome-flags.conf`` Chrome config.
- ``icons/`` Icons.
   - ``default/`` Defaults.
      -``index.theme`` Cursor theme.
     

Link/copy configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are two types of configuration files in the ``dotfiles`` directory.

1. Configuration files that are meant to be user-edited.
2. Configuration files that are not supposed to be modified.

User-defined configuration files are supposed to be edited by the users according to their system and likings.
These files contain system-specific configurations that cannot be shared across computers.
Therefore, these files shouldn't be linked to the user's home directory.
Instead, they are copied from the repository to the home directory.
And if the files existed in the home directory, they should be merged manually.
The repository contains a script called ``copy-dotfiles.sh`` that copies configuration files from the list ``dotfiles-copy-list.txt``.
To run it, simply type

.. code-block:: bash

   ./copy-dotfiles.sh

It copies the required configuration dotfiles to the user's home directions or create files with ``.merge`` extension if the configuration
files already existed.
To merge the files, use an editor to edit the ``*.merge files`` and use ``mv`` to replace the original file, for example:

.. code-block:: bash

   mv .myconfig.merge .myconfig

For configuration files that aren't supposed to be modified, they can be linked to the home directory using the script ``link-dotfiles.sh``.

.. code-block:: bash

   ./link-dotfiles.sh
   
**Caution**, it creates numbered backup files before linking the configuration files.

Therefore, if you don't want the home directory to contain a lot of backup files, **use this script once only**.
These configuration files will be automatically update when you pull from the origin.

Edit configurations
^^^^^^^^^^^^^^^^^^^
Feel free to modify any files as listed in ``dotfiles-copy-list.txt``.

However, there are several settings in the configurations in the dotfiles that needed user input for things to work properly.

**Note**: Do not modify the configuration files in the cloned repository.
Instead, modify those already linked/copied to your home directory.

Qtile
#####
CPU temperature sensor and WiFi interface
Modify ``~/.config/qtile/config.ini``

.. code-block:: bash

   # ~/.config/qtile/config.ini
   ...
   [wlan]
   interface = wlp3s0  # Use ip addr or nmcli command to find your WiFi interface and put it here.
   ...
   [thermal sensor]
   tag_sensor = Package id 0  # Use sensors command to find the sensor tag of the CPU temperature sensor. Requires the lm-sensors package.
   ...

You don't need to modify other ``.ini`` files for Qtile to work.
But, if you wish, modify other values as well.

(optional) Ly
#############
To change the foreground color, modify ``/etc/ly/config.ini``.

.. code-block:: bash

   # /etc/ly/config.ini
   ...
   term_reset_cmd = /usr/bin/tput reset; /usr/bin/printf/ "%b" "\e]P700FF66\ec"
   ...

Here, at the last bit of this config, ``P7`` refers to the foreground color and ``00FF66`` is the HEX value of my favorite terminal green color.

In addition, modify ``/usr/lib/systemd/system/ly.service``.

.. code-block:: bash

   # /usr/lib/systemd/system/ly.service
   ...
   [Service]
   ...
   ExecStartPre=/usr/bin/printf "%%b" "\e[P700FF66\ec"  # Add this line.
   EXecStart=.....
   ...

(optional) Select default audio card
####################################
To list all audio cards, type

.. code-block:: bash

   cat /proc/asound/cards

Identify the desired default audio card and then create ``/etc/asound.conf``

.. code-block:: bash

   # /etc/asound.conf
   defaults.pcm.card 1
   defaults.ctl.card 1

and replace ``1`` with the desired card number.
Re-login to take effect.

Install optional packages
-------------------------
Install optional packages in ``pkglist-optional.txt``
Here are applications that I use, but may not be necessary.

.. code-block:: bash

   # pkglist-optional.txt
   cups  # For printing
   zoom  # Remote meeting
   vlc  # Video player
   qbittorrent  # Torrent
   virtualbox  # Virtual machine
   virtualbox-host-modules-arch
   feh  # Image viewer
   texstudio  # Latex
   textext-git  # Inkscape latex extension
   inkscape  # SVG drawer
   smartmontools  # S.M.A.R.T utitlies for storage drives
   remmina  # Remote control
   timeshift  # Backup
   unzip  # Unzip...
   

Set up and configurations
^^^^^^^^^^^^^^^^^^^^^^^^^
CUPS
####
For my HP Officejet 4630, install ``hplip`` package.

Enable and start ``cups.service``

.. code-block:: bash

   systemctl enable cups.service
   systemctl start cups.service

Go to a browser and type ``localhost:631`` to access the CUPS server.

Select the ``Administration`` tab to add and setup printers.

timeshift
#########
Enable ``cronie.service``.

.. code-block:: bash

   sudo systemctl enable cronie.service
   sudo systemctl start cronie.service

Type

.. code-block:: bash

   sudo timeshift-gtk

To open the timeshift GUI.

I am a first time ``timeshift`` user.
I backup daily (5 copies), weekly (3 copies), and monthly (2 copies) and
I backup my user hidden files.

Cheatsheet, Perks, and Miscellaneous
====================================
Grub
----
Audio playback
--------------
Kernel parameters
-----------------
Keychron K1 function keys
-------------------------
To enable my keychron K1 function keys, create ``/etc/modprobe.d/hid_apple``
and add the following line

.. code-block:: bash

   # /etc/modprobe.d/hid_apple.conf
   options hid_apple fnmode=0
