# Architecture

## Content structure

- `_posts/` — Jekyll naming convention `YYYY-MM-DD-title.md`
- `_layouts/` — `last-week.html` (weekly roundup), `post.html` (standard), `tag_page.html`, `tag_feed.xml`
- `_includes/` — header, footer, breadcrumbs, youtube embeds, etc.
- `_config.yml` — Minima theme; plugins jekyll-feed, jekyll-category-pages, jekyll-sitemap, jekyll-paginate (5 posts/page)
- `_data/authors.yml` — author info referenced via `page.author`
- `_plugins/ext.rb` — loads jekyll-tagging

## Automated workflows (`.github/workflows/`)

1. **last-week.yml** — weekly (Sundays 14:01 UTC) or on-demand. Runs `.github/scripts/get_interesting_news.py` to fetch saved links, creates a new `_posts/` markdown post, commits and pushes, Slack-notifies.
2. **jekyll.yml** — builds (Ruby 3.1, Jekyll 4.3) and deploys to GitHub Pages. Triggered by pushes to `master` **or after last-week.yml completes** — so a weekly post's own commit is what triggers its deploy, not a separate scheduled build.

## Post front matter

```yaml
---
layout: last-week  # or 'post' for regular posts
title: Some things I found interesting from 2024-06-30 to 2024-07-07
category: Last-Week
tags: []
author: pgmac
---
```
