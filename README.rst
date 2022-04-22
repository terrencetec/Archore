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

.. code-block::

   mkfs.ext4 /dev/partition

For storage partitions shared with Windows

.. code-block::

   mkfs.ntfs /dev/partition

For swap partition

.. code-block::

   mkswap /dev/swap_partition

For EFI partition

.. code-block::

  mkfs.fat -F 32 /dev/efi_partition
  
Mounting the partitions
-----------------------
Mount root partition

.. code-block::
   
   mount /dev/root_partition /mnt
   
Mount EFI partition

.. code-block::

   mount --mkdir /dev/efi_partition /mnt/efi

Mount other partitions

.. code-block::

   mount --mkdir /dev/other_partitions /mnt/other_mount_points
   
Enable swap

.. code-block::

   swapon /dev/swap_partition
   
   
Update mirror list
------------------
Use reflector

.. code-block::

   reflector --country country --protocol https --sort score --save \etc\pacman.d\mirrorlist
   
| Replace ``country`` with a comma separated list, e.g. ``Hong\ Kong,Japan``.
| To get a list of countries, run

.. code-block::

   reflector --list-countries | less
   
Install essential packages
--------------------------
Use pacstrap

.. code-block::

   pacsctrap /mnt base base-devel linux linux-headers linux-firmware linux-lts linux-lts-headers
   
``linux-lts`` and ``linux-lts-headers`` are optional.

| Append the following list of packages as appropriate.
| **Only install packages that are required for the installation process.**
| Other user packages can be installed after the installation.

.. code-block::
   
   vim git man-db man-pages texinfo ntfs-3g networkmanager 
   
Configure the system
--------------------
Fstab
^^^^^

.. code-block::

   genfstab -U /mnt >> /mnt/etc/fstab
   
Check result in /mnt/etc/fstab in case of error.

Chroot
^^^^^^
.. code-block::

   arch-chroot /mnt
   
Time zone
^^^^^^^^^
.. code-block::
   
   ln -sf /usr/share/zoneinfo/Region/City /etc/localtime
   
run ``hwclock`` to generate ``/etc/adjtime``

.. code-block::

   hwclock --systohc
   
Localization
^^^^^^^^^^^^


