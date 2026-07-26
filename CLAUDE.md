# CLAUDE.md

Jekyll blog on GitHub Pages (`https://pgmac.net.au`), with a weekly "interesting last week" post auto-generated from saved links. Full architecture: `docs/ARCHITECTURE.md`.

## Commands

```bash
bundle install
bundle exec jekyll serve   # local dev
bundle exec jekyll build   # -> _site/
```

Weekly script (`.github/scripts/get_interesting_news.py`) needs `consumer_key` and `access_token` (Pocket API, lowercase — not the usual `POCKET_*` shape) plus `PGLINKS_KEY` (links.pgmac.net.au).

## Gotchas

- Jekyll dev server does not auto-reload `_config.yml` changes — restart it
- `jekyll.yml` (build+deploy) fires on push to `master` **or** after `last-week.yml` finishes — a weekly post is what triggers its own deploy, there's no separate scheduled build
