---
layout: post
title: Incidents and status
category: sre
tags: [sre, incidents, status]
author: pgmac
---

I've decided to take a leaf out of my professional life and apply that to some of my homelab life (because it is life!).

So here I am doing some public incident management of stuff that should have little to any affect on people outside my home.

This is made up of a couple of pieces:

1. Recording my incidents with rigor
2. Advertising the public facing things

To do option 1, I cheated. I used to Claude Code to grab a bunch of information, even perform a bunch of actions, collate it all together, process it with some rules and create a markdown file with the analysis.

To do option 2, I cheated. I used Claude Code to take the status from my home Nagios monitoring system, pick out some important hosts and services and display that status on a public website.

## Option 1 - incident docs

To record and display this, I'm keeping the markdown docs in a [repo](https://github.com/pgmac-net/incidents/) and using mkdocs to generate html files and serve on a my [Incidents site](https://incidents.pgmac.net.au/docs/) (hosted by GitHub Pages).

## Option 2 - Public Status page

I created and open sourced a python API to grab the status of some carefully selected Nagios hosts and services. Then, I grab this with a vue.js front end to make it look pretty.

I preseent to you, the very aptly named: [nagios-public-status-page](https://github.com/pgmac-net/nagios-public-status-page)
