---
layout: post
title: An index of tag feeds
permalink: /feed/tags/
---

Here you'll find the RSS/Atom feeds for the tags I use across the site. You can subscribe to one (or more) of these in your own clients to keep up to date with article I post.
Some work, some don't. I have some cleanup to do - I _may_ get to that at some stage.

Thanks!

{% assign sorted_tags = site.tags | sort %}
{% for stag in sorted_tags %}
[{{stag[0]}}](/feed/tags/{{stag[0] | slugify }}.xml)
{% endfor %}
