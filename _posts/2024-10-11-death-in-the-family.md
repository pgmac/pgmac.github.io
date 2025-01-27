---
layout: post
title: A death in the (hardware) family
category: Tech
tags: ['samba', 'hardware', 'death']
author: pgmac
---

Looks like we had a death in the family yesterday 😢 

My really old HP ProLiant MicroServer looks to have suffered either a fatal IO bus problem, or hard drive failure 🪦 

I'm thinking IO bus more than HDD (yes, it is an HDD in there) because the whole server either freezes or reboots whenever it tries to read data.
I might get a few seconds to approx a minute of boot-up before it borks and goes back to sleep. I did briefly see some ata sector errors during boot-up before it all went away. Not long enough to get any actual detail, though. I haven't seen that kind of behaviour for a HDD failure, which leads to me think IO bus and/or mainboard.

Oh well, good thing it only ran my internal samba server, everything else had already been migrated off. I did want to move samba off as well - I even started researching what I'd need to do. Just never got around to actually doing it. Looks like that work has now been prioritised. Of course I had no backups of the AD. I do have details for the DNS that was on there, though. I've managed to replicate that on my pfSense firewall to get things going again.

I might look at running samba in my microk8s cluster now. That way it'll all be "as code" and won't be quite so bad if/when things fail again.

It led a rich and fulfilling life. It deserves it's rest. I would have liked to decommission it nicely, though. We don't always get to chose how we go.
