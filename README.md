# Tech Deals Tracker – Under £100

Automated affiliate site that aggregates tech deals under £100, builds static pages, and deploys to a free host. No content grind.

## Features
- Scheduled auto‑updates (every 4h)
- Category pages + Top 30 homepage
- Freshness + de‑dup + scoring
- Affiliate‑ready buttons & disclosures
- Sitemap/robots for SEO

## Deploy
1. Fork/repo → add files.
2. Set repo secrets (AWIN/AMZN/eBay keys, SITE_BASE_URL).
3. Connect Cloudflare Pages → build cmd:
   ```
   pip install -r requirements.txt && python scripts/fetch_deals.py && python scripts/curate_deals.py && python scripts/build_site.py
   ```
4. Hit your site URL.

## Local Dev
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export SITE_BASE_URL=http://localhost:8000
python scripts/fetch_deals.py && python scripts/curate_deals.py && python scripts/build_site.py
python -m http.server -d site 8000
```

## Config
- Edit `config.yml` for categories, filters, max price, etc.
- Enable real merchant adapters once approved; keep `mock_local` for demo.

## Monetisation
- Add AdSense code snippet into `base.html` (head/body) once approved.
- Affiliate links live in each deal’s `url`.

## Roadmap
- Multi‑merchant compare block
- Telegram/Discord alert bot (reads `data/email_digest.json`)
- Click tracking via Bitly/GeniusLink
- Simple API: expose `data/deals_curated.json` via `/api/` folder
