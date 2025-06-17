---
layout: post
title: AWS Internet access from a Private subnet
category: Technology
tags: [aws, networking]
author: pgmac
---
To enable internet access from a private subnet, you will need do a couple of things.

1. Create a new public subnet (if you don't have one already)
1. Create an Internet Gateway and associate it with this public subnet, making it the default gateway
1. Create a NAT Gateway associated with this public subnet (it must have a public subnet IP address)
1. Set the default route (in the Routing Tables) for the private subnet to be the NAT Gateway we just created.
1. Pull things from the internet
