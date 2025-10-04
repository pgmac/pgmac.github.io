# GitHub Copilot Instructions

This file provides guidance to GitHub Copilot when reviewing code and suggesting changes in this repository.

## Project Overview

This is a Jekyll 4.3-based static blog deployed to GitHub Pages. The site features automated weekly content generation from a link management API.

## Code Review Focus Areas

### Jekyll Configuration
- Verify `_config.yml` changes don't break existing functionality
- Remind that config changes require restarting `bundle exec jekyll serve`
- Ensure new plugins are added to both `gems:` and `plugins:` sections in `_config.yml`
- Check that new plugins are also added to the `Gemfile`

### Post Front Matter
- Verify all posts in `_posts/` follow naming convention: `YYYY-MM-DD-title.md`
- Ensure front matter includes required fields:
  - `layout:` (typically `post` or `last-week`)
  - `title:`
  - `category:`
  - `tags:` (can be empty array)
  - `author:` (must match a key in `_data/authors.yml`)
- Check dates in filenames match reality (especially for future-dated posts)

### Layout and Template Changes
- Verify Liquid template syntax is correct
- Check that layout changes maintain responsive design
- Ensure new layouts properly extend `default.html` or other base layouts
- Validate schema.org microdata attributes are correct

### GitHub Actions Workflows
- Check that workflow syntax is valid YAML
- Verify cron schedules use correct syntax
- Ensure secrets are referenced properly with `${{ secrets.SECRET_NAME }}`
- Check that workflow permissions are appropriate and not overly broad
- Verify Slack notification payloads are valid JSON
- Ensure Python scripts have proper error handling

### Python Scripts
- Verify scripts use Python 3.12+ compatible syntax
- Check that required environment variables are documented
- Ensure proper error handling with try/except blocks
- Verify API calls have appropriate timeouts
- Check that requests use proper headers and authentication

### Dependencies
- Ensure Gemfile.lock is updated when Gemfile changes
- Verify version constraints are reasonable (use `~>` for minor version flexibility)
- Check for security vulnerabilities in dependencies

### Content Quality
- Flag posts with empty or missing content
- Check for broken internal links
- Verify tag names are consistent (case-sensitive)
- Ensure author references exist in `_data/authors.yml`

## Common Patterns

### Creating New Posts
Posts should be created in `_posts/` with:
- Filename: `YYYY-MM-DD-descriptive-title.md`
- Front matter with all required fields
- Content in markdown format

### Adding Custom Includes
Reusable components go in `_includes/` and are referenced in templates with:
```liquid
{% include component-name.html %}
```

### Tag System
- Tags are defined in post front matter as arrays
- Tag pages are auto-generated via jekyll-category-pages plugin
- Tag feeds are generated using `tag_feed.xml` layout

## Deployment Notes
- Main branch is `master` (not `main`)
- Site deploys automatically on push to master
- Both build and deploy must succeed for changes to go live
- Check GitHub Actions status if changes don't appear on site
