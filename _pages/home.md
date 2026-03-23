---
permalink: /notes/
title: "Notes"
excerpt: "My notes posts"
author_profile: true
---

#Blog

{% assign posts = site.note | sort: "date" | reverse %}
{% for post in posts %}

[{{ post.title }}]({{ post.url }}){% if post.date %} ({{ post.date | date: "%Y-%m-%d" }}){% endif %}
{% endfor %}