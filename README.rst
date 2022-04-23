Arch-core
==========
Core scripts, templates, configuration files, and instructions for setting up my Arch Linux.

Installation
============
| Follow the instructions below.
| When in doubt, follow `installation guide <https://wiki.archlinux.org/title/Installation_guide>`_ in ArchWiki.

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
   
   vim git man-db man-pages texinfo ntfs-3g networkmanager 
   
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
   
run ``hwclock`` to generate ``/etc/adjtime``

.. code-block:: bash

   hwclock --systohc
   
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

.. code-block::

   # /etc/hostname
   myhostname
   
| I use the following convention for ``myhostname``: *name-OS*, e.g. ``Terrence-Linux``.
| If necessary, add suffix to avoid ambiguity, e.g. ``Terrence-Linux-1`` or ``Terrence-Linux-5900X``.

Root password
^^^^^^^^^^^^^
Type

.. code-block::

   passwd
   
and set the root password

Microcode
^^^^^^^^^
Install ``intel-ucode`` for Intel processors or ``amd-ucode`` for AMD processors:

.. code-block::

   pacman -Syu intel-ucode

or

.. code-block::

   pacman -Syu amd-ucode

Boot loader
^^^^^^^^^^^
Install ``grub`` and ``efibootmgr`` (and ``os-prober`` if dual boot)

.. code-block::

   pacman -Syu grub efibootmgr os-prober

Edit the following in ``/etc/default/grub``

.. code-block::

   # /etc/default/grub
   ...
   GRUB_DEFAULT=saved
   ...
   GRUB_SAVEDEFAULT=true
   ...
   GRUB_DISABLE_SUBMENU=y

After making changes in ``/etc/default/grub``, remember to generate ``/boot/grub/grub.cfg`` by typing

.. code-block::

   grub-mkconfig -o /boot/grub/grub.cfg

Post installation
=================
Feel free to reboot and remove the installation media or simply continue working on it.

Install Paru
------------
