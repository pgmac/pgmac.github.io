---
layout: post
title: Extending/resizing a logical volume file system
category: Technology
tags: [lvm, pv, lv]
author: pgmac
---
In my infinite wisdom, I recently decided to "Just add more disk" to address a problem I was having with garbage collection.
I wanted to add another 16GB of storage to my LVM filesystem to just stop my monitoring from carrying on about there being <20% available.
Plus, the microk8s garbage collection was being garbage.

I'm using proxmox as my virtualisation layer, so adding more disk on was dead easy. I'll leave that as an exercise for the reader.

Increasing my LVM root partition was a little more involved.
But, in the end, it came down to just a few commands:

`lsblk` This will list information about your block devices attached to your system

`pvresize` This resizes the Physical Volume attached to the LVM

`vgs` This gives information about the Volume Group(s)

`pvs` This gives information about the Physical Volume(s)

`lvextend` This does the magic

The combination of these that makes the magic work is:

1. `lsblk`<br/>
   List out your block devices and note the one you increased the storage on
2. `pvresize /dev/sda3` <br/>
   Resize the Physical Volume to match the new size
3. `lsblk`<br/>
   Give it the once over to make sure the new numbers are applied
4. `vgs`<br/>
   Look at the Volume Group to see how it's looking
5. `pvs`<br/>
   Look at the Physical Volumes to see how they're going
6. `lvextend -r -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv`<br/>
   Here's the good bit. This extends the Logical Volume AND the file system (-r) to the full size of the newly resized Physical Volume
7. `df`<br/>
   Gaze in wonder at all the additional storage you have available to you now

Other commands that might be helpful:

Have a look at their manpages and/or --help system

1. `partprobe`<br/>
   This informs the operating system about partition table changes.
2. `growpart`<br/>
   This will rewrite the partition table so the partition takes up all the space it can
3. `resize2fs`<br/>
   The resize2fs program willresize ext2, ext3, or ext4 file systems.
4. `fsadm`<br/>
   This utility checks or resizes the filesystem on a device.
5. `fdisk`<br/>
   Display or manipulate a disk partition table.