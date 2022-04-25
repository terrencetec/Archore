Arch-core
==========
Core scripts, templates, configuration files, and instructions for setting up my Arch Linux.

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

   [iwd]# station device get-network

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
|/          |Linux root (x86-64)|Reminder                    |
+-----------+-------------------+----------------------------+

Storage drive
^^^^^^^^^^^^^
+-------------+-----------------------+----------------------------+
|mount point  |partition type         |size                        |
+=============+=======================+============================+
|/storage     |Linux filesystem       |Reminder                    |
+-------------+-----------------------+----------------------------+
|/storage2    |Microsoft storage space|Reminder                    |
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

   reflector --country country --protocol https --sort score --save \etc\pacman.d\mirrorlist

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
   zh_hk.UTF-8 UTF-8
   ...

After that, run

.. code-block:: bash

   locale-gen

Create ``/etc/locale.conf`` and set the ``LANG`` variable

.. code-block:: bash

   # /etc/locale.conf
   LANG=en_US.UTF8 UTF8

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

   git clone https://github.com/terrencetec/Arch-core.git
   
Or, use ssh if you are me. In this case, generate ssh-key and upload it to GitHub prior to this.

.. code-block:: bash

   ssh-keygen -t ed25519 -C "terrencetec@gmail.com"

| And find the public key in where it is generated and somehow copy the thing to GitHub.
| Then, clone with ssh   

.. code-block:: bash

   git@github.com:terrencetec/Arch-core.git
   
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

Install them using ``paru``.

.. code-block:: bash
   
   cd Arch-core
   paru -S - < pkglist-core.txt

Alternatively, add the ``--needed`` tag to avoid reinstalling packages

.. code-block:: bash

   paru -S --needed < pkglist-core.txt

Python dependencies for my qtile configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Optionally, install required Python packages for qtile.

.. code-block::

   pip install iwlib psutils


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
Copy dotfiles from the repository to home directory.

.. code-block::

   cp dotfiles/.* ~ -r

Do this with caution as it overwrites the original dotfiles.

The dotfiles directory contains

- ``.bashrc``  # BASH initiation script
- ``.xprofile``  # Shell scripts for autostarting
- ``.Xdefaults``  # Configurations for urxvt and others. Notice other dependencies.
- ``.Xresources``  # Other configurations, cursors, etc...
- ``.vimrc``  # Configuration for vim. Remember to install extensions.
- ``.inputrc``  # My skipword shortcut.
- ``imwheelrc``  # IMWheel config. Install ``imwheel`` for this to take effect.
- ``.config/``  # .config directory containing
  - ``chrome-flags.conf``  # Chrome config to avoid dropdown menus issues.
  - ``qtile/``  # Qtile configs.
  - ``picom/``  # Picom configs. Install ``picom`` for this to take effect.
  - ``rofi/``  # Rofi configs.
