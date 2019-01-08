---
layout: post
title: How-To extend a Logical Volume using LVM on Linux
category: Technology
author: pgmac
---
While not a difficult process, it's not the easiest of things to do either. Logical Volume Manager (LVM) lives up to *NIX's user friendly mantra - "UNIX is user friendly, it's just picky about who it's friends are".

Because LVM is actually really powerful and flexible in managing your storage, this inherently means complexity maintaining/controlling LVM.

The basic process to extend a Logical Volume goes like this:

1. Add the additional storage to your system.
   Whether physical disks, additional virtual storage, or extending existing storage — whatever best suits your situation, needs and available resources.

2. Create a file system on the additional storage.
   You can use fdisk, gparted, or another — again, I'll leave this up to you.
   My new file system is '/dev/sda3'

3. Prepare the new partition for use by LVM
   pvcreate /dev/sda3

4. List the available Volume Groups on your system

   ```vgdisplay | grep 'VG Name```

   My VG is named 'ubuntu-vg':

5. Extend the appropriate Volume Group (VG)

   ```vgextend ubuntu-vg /dev/sda3```

Next we need to update the appropriate Logical Volume.

1. First, list out your LV's:

   ```lvdisplay | egrep "LV (N|P)a(m|t)(e|h)"```

   This will/should return both the "LV Name" and "LV Path" configuration items.
   I want to extend the 'root' LV on path '/dev/ubuntu-vg/root'

1. Now we have enough information to resize the LV

   ```lvresize -r -l 100%VG /dev/ubuntu-vg/root```

1. Lastly, we need to resize the filesystem to match the LV

   ```resize2fs /dev/mapper/ubuntu--vg-root```

Anyway, that's a very quick way to get it done.
It helped me, I hope it helps you, too.