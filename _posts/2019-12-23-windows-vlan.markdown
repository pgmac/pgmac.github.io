---
layout: post
title: Windows Server Virtual Interface with a configured VLAN with a custom MAC
category: Technology
tags: [Windows, Server, VLAN]
author: pgmac
---

I'm not a Windows server kinda guy, but do you think I could find a nice, easy to follow, walk-through on how to create a Windows Server Virtual Interface on a given VLAN and using a custom MAC?
No, no I couldn't. Perhaps I wasn't searching with the correct search terms. Perhaps this is assumed knowledged on a Windows Server. I don't know.
But, here is how I ended up solving my problem.

****

1. The problem

We have a Windows Server. It's going to be our internal, non-production, database server.
But, it's going to host multiple databases for multiple environments (dev, sit, uat, etc, etc).
We split and protect each of our environments using VLAN's.

2. The requirements

The server needs to have multiple VLAN's attached to it.
The server has 2x 10GB NIC's.
These 2 NIC's must be configured for automatic failover, to protect us in the event of failure of cable/switch/port/etc. We'll be using "NIC Teaming" for this.
The VLAN Virtual Interfaces need to have their own, individual, MAC. NIC teaming still uses the base, physical/teamed, card's MAC for the VLAN Virtual Interface(s).

3. The solution

3.1 Create the NIC Team and provision the Virtual Interface

a. Create the NIC Team of the 2x 10GB NIC's. There are plenty of great guides on how to do this. Have a search around, I'll try to link one that I used ... sometime.
b. Configure this to be "Switch Independent" and "Dynamic".
c. Configure the first NIC to be the primary and the second to be the "failover".
d. Now - go the "TEAMS" section and click on the NIC Team you just created.
e. Under the "ADAPTERS AND INTERFACES", select the "Team Interfaces".
f. At the top-right, there is a dropdown box labelled "TASKS". Click this and select the "Add Interface" menu item.
g. Give it a meaningful Name and VLAN.

Now you should have a new Virtual Interface on a the needed VLAN, but it still has a "shared" MAC and it doesn't have an IP address yet.

3.2 Configure the Virtual Interface

First we'll give it the custom MAC

a. Got the properties of the new Virtual Interface
b. Click on the "Configure" button
c. Click on the "Advanced" tab
d. In the list box, find the "MAC address" item and click on it.
e. You'll now be able to enter a custom MAC for this Virtual Interface. I usually just add "1" (in hex, obviously) to the base NIC.

Now  we have that, we can give it an IP address. I gave mine a static IP address, but now that you have a custom MAC, you should be able to DHCP it, too.

a. Still in the Virtual Interface "Properties", configure t5he IPv4 settings.
b. Select "static"
c. Enter the required IP address
d. Enter the Netmask
e. Enter the Gateway. This is actually required, otherwise you won't be able to access the new interface properly. Windows will prompt you, asking if you _really_ want to do this. You do _really_ want to do this.

It should be all good to go now.
Assuming the Windows Firewall doesn't get in your way. But, that's a different story.
