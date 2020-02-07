---
layout: post
title: Tricks and Traps with pfSense and CARP configurations
category: Technology
tags: [Networks, Firewall, VLAN, High Availability]
author: pgmac
---

pfSense Tricky trickness

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

# BGP configuration

## Neighbors

Neighbors need to be configured.
I have only seen the "Raw Config" optiont to add in neighbors. You need to configure the source(/local) address and the remote address. The MD5 auth password could be optional, but I've only even configured them with a MD5 auth password.
The logs aren't always helpful when trying to diagnose what's happening. I found doing a tcpdump on the pfSense hosts gave me more information.
tcpdump -ni eth0 port 179
Without the MD5 auth password, I'd see messages like:
"md5 shared secret not supplied with -M, can't check - <md5 hash>"

The BGP Neighbor status will be shown as "Active" - which is actually very bad and means that nothing is happening.

### BGP neighbor states

*Active*: Not doing anything, not talking to any one. The exact opposite of "Active". This is likely a configuration problem with the neighbor (MD5 auth password, etc).
*Connect*: It's trying to connect to the neighbor, but is likely having problems. Firewalls and routes are things to look at here.
*Established*: It's alive! Things are good, routes are advertised. You should be good to go.
