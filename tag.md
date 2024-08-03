---
layout: post
title: Tag
permalink: /tag/
---

I have too many tags, here they all are

{% assign sorted_tags = site.tags | sort %}
{% for stag in sorted_tags %}
[{{stag[0]}}](/tag/{{stag[0] | slugify }})
{% endfor %}
