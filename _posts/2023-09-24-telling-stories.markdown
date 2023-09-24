---
layout: post
title: Telling stories
category: Family
tags: [Family, Stories]
author: pgmac
---

As we were driving south to start our family holiday, it was getting late at night and my son was getting very tired and refusing to go to sleep without a proper good night story - he loves his good night stories.
We normally read him a story and a couple of kids meditations.
This night we were driving, mum was already asleep in the back with our daughter - also asleep.
Here I am driving and having a story demanded of me.
I can't read him a story, I'm driving.
I'll have to make one up.
I'm not the best at making up stories, but every now and then things come together and pull some magic out - or at least something that works.
These are the stories I made up while driving.

<ul class="posts">
{% for post in site.tags.Stories limit: 20 %}
  <div class="post_info">
    <li>
         <a href="{{ post.url }}">{{ post.title }}</a>
         <span>({{ post.date | date:"%Y-%m-%d" }})</span>
    </li>
    </div>
  {% endfor %}
</ul>

****

{% for category in page.categories %}
  {% assign moreThanOneInCategory = false %}
  {% assign posts = site.categories[category] %}

  {% for post in posts %}
    {% if forloop.length > 1 %}
      {% assign moreThanOneInCategory = true %}
    {% endif %}
  {% endfor %}
  {% if moreThanOneInCategory == true %}
    <div class="related-posts">
      <h3>Other posts archived in “{{ category }}”</h3>
      <ul>
        {% for post in posts %}
          {% unless post.url == page.url %}
            <li>
              <a href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>

              Published on <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %-d, %Y" }}</time>
            </li>
          {% endunless %}
        {% endfor %}
      </ul>
    </div>
  {% endif %}
{% endfor %}
