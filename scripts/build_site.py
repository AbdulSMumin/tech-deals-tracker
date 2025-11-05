import os, json, yaml
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from scripts.utils import read_json, now_utc

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(ROOT / 'config.yml', 'r', encoding='utf-8'))

# Set last_updated at build time (UTC, but we’ll label as GMT in display)
CFG['site']['last_updated'] = now_utc()

env = Environment(
    loader=FileSystemLoader(str(ROOT / 'templates')),
    autoescape=select_autoescape(['html', 'xml'])
)

# Jinja filter to format ISO timestamp nicely as "06 Nov 2025, 01:00 GMT"
def format_datetime(value):
    try:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%d %b %Y, %H:%M GMT")
    except Exception:
        return value

env.filters["format_datetime"] = format_datetime

site_out = ROOT / 'site'
(site_out / 'categories').mkdir(parents=True, exist_ok=True)

curated = read_json(str(ROOT / 'data' / 'deals_curated.json'), [])

home_deals = curated[: CFG['site']['max_homepage']]
index_tpl = env.get_template('index.html')
(site_out / 'index.html').write_text(
    index_tpl.render(cfg=CFG, deals=home_deals),
    encoding='utf-8'
)

cat_tpl = env.get_template('category.html')
for c in CFG['site']['categories']:
    slug = c['slug']
    cd = [d for d in curated if d.get('category') == slug]
    out_dir = site_out / 'categories' / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'index.html').write_text(
        cat_tpl.render(cfg=CFG, cat=c, deals=cd),
        encoding='utf-8'
    )

sm_tpl = env.get_template('sitemap.xml')
(site_out / 'sitemap.xml').write_text(sm_tpl.render(cfg=CFG), encoding='utf-8')

rb_tpl = env.get_template('robots.txt')
(site_out / 'robots.txt').write_text(rb_tpl.render(cfg=CFG), encoding='utf-8')

print("Site built → ./site")
