---
layout: post
title: Search Results
permalink: /search/
---
<!-- List where search results will be rendered -->
<ul id="search-results"></ul>

<script>
  // Template to generate the JSON to search
  window.store = {
    {% for post in site.posts %}
      "{{ post.url | slugify }}": {
        "title": "{{ post.title | xml_escape }}",
        "author": "{{ post.author | xml_escape }}",
        "category": "{{ post.category | xml_escape }}",
        "content": {{ post.content | strip_html | strip_newlines | jsonify }},
        "url": "{{ post.url | xml_escape }}"
      }
      {% unless forloop.last %},{% endunless %}
    {% endfor %}
  };
</script>

<script src="https://unpkg.com/lunr/lunr.js"></script>
<script src="/js/search.js"></script>
