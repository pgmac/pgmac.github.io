---
layout: post
title: Tricks and Traps with pfSense and CARP configurations
category: Technology
tags: [Networks, Firewall, VLAN, High Availability]
author: pgmac
---

Tricky trickness

# CARP

## Use unique VHID's everywhere.

using the same VHID for your CARP VIP can cause confusion (and delay). Especially when using CARP on two, or more, hosts on the same subnet.
EG: a data centre to data centre direct link (Virtual Cross Connect/VXC).
If hosts on either end are on the same subnet (which they kinda should be) AND you have CARP configured to enable High Availability (HA) on both pfSense hosts AND both of the CARP VIP's are configured with the same VHID, the pfSense boxes will be confused about which VIP should be associated with which pfSense box.
This is because CARP uses multicast to determine which host is the "live" host. With 2 hosts on the same subnet, both of them will be receiving the multicast packets. This means each one will be trying to take control of all available VIP's.
This can mean the VIP meant for one end of the link can actually end up on the other end of the link - which obviously breaks things.

## Symptoms seen during this.

Connectivity is intermittent.
pings may start and stop randomly
tcp connections fail

# Configuration sync-ing

pfSense only sync the base pfSense configuration items. They don't sync the configuration for any third party packages.
I understand the decision for this, but it can be frustrating when your Highly Available pair of pfSense boxes don't work properly. Especially when BGP (frr) is involved.
