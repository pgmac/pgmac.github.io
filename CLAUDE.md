# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Jekyll-based static blog hosted on GitHub Pages at https://pgmac.net.au. The site features regular blog posts, a special "interesting last week" series that's automatically generated from saved links, and tag-based organization.

## Common Commands

### Local Development
```bash
# Install dependencies
bundle install

# Run local development server
bundle exec jekyll serve

# Build the site (outputs to _site/)
bundle exec jekyll build
```

### Weekly Content Generation
The `.github/scripts/get_interesting_news.py` script generates weekly "interesting last week" posts:
```bash
# Run manually (requires environment variables)
.github/scripts/get_interesting_news.py
```

Required environment variables:
- `consumer_key` - Pocket API consumer key
- `access_token` - Pocket API access token
- `PGLINKS_KEY` - API key for links.pgmac.net.au

## Architecture

### Content Structure
- **Posts**: Located in `_posts/` following Jekyll naming convention `YYYY-MM-DD-title.md`
- **Layouts**: Custom layouts in `_layouts/` including:
  - `last-week.html` - Special layout for weekly roundup posts
  - `post.html` - Standard blog post layout
  - `tag_page.html` - Tag archive pages
  - `tag_feed.xml` - RSS feeds for individual tags
- **Includes**: Reusable components in `_includes/` (header, footer, breadcrumbs, youtube embeds, etc.)

### Automated Workflows
Two GitHub Actions workflows in `.github/workflows/`:

1. **last-week.yml**: Runs weekly (Sundays at 14:01 UTC) or on-demand
   - Executes Python script to fetch saved links from a link management API
   - Creates a new markdown post in `_posts/` with links from the previous week
   - Commits and pushes the new post
   - Sends Slack notifications about build status

2. **jekyll.yml**: Builds and deploys the site to GitHub Pages
   - Triggered by pushes to master or after last-week workflow completes
   - Runs `bundle exec jekyll build`
   - Deploys to GitHub Pages
   - Sends Slack notifications

### Configuration
- **_config.yml**: Main Jekyll configuration
  - Site uses the Minima theme
  - Plugins: jekyll-feed, jekyll-category-pages, jekyll-sitemap, jekyll-paginate
  - Pagination set to 5 posts per page
  - Tag pages configured with custom layouts

- **_data/authors.yml**: Author information referenced in post templates via `page.author`

- **_plugins/ext.rb**: Loads the jekyll-tagging plugin for tag functionality

### Post Front Matter
Standard posts use this front matter structure:
```yaml
---
layout: last-week  # or 'post' for regular posts
title: Some things I found interesting from 2024-06-30 to 2024-07-07
category: Last-Week
tags: []
author: pgmac
---
```

### Deployment
The site is automatically deployed to GitHub Pages when changes are pushed to the `master` branch. The build process uses Ruby 3.1 and Jekyll 4.3.

## Notes
- Config changes require restarting the Jekyll server (not auto-reloaded)
- The site uses kramdown for markdown processing
- Tag pages are automatically generated via the jekyll-category-pages plugin
