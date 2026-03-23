---
permalink: /blog/
title: "Blog"
excerpt: "My blog posts"
author_profile: true
---

#Blog

{% assign posts = site.blog | sort: "date" | reverse %}
{% for post in posts %}

[{{ post.title }}]({{ post.url }}){% if post.date %} ({{ post.date | date: "%Y-%m-%d" }}){% endif %}
{% endfor %}