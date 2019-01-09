---
layout: post
title: JVC Everio MOD files to MPG
category: Technology
tags: [Video, Conversions]
author: pgmac
---
I keep needing to convert the MOD files from my JVC Everio video camera to MPEG4 files, ready for building into a DVD. And everytime I keep going back to Google to find the commands. I don't do it often enough to remember it, I don't even do it often enough to remember to script it.
So, with that in mind, I'm putting it up here so it can hide somewhere.

`avconv -i <input MOD file> -vcodec mpeg4 -b 2300k -filter:v yadif -aspect 16:9 -c:a copy <output MPG file>`
