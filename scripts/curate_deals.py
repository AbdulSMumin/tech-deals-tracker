import json, yaml
from pathlib import Path
from scripts.utils import (
    read_json,
    write_json,
    pass_filters,
    score_deal,
    categorise,
    add_affiliate_tag
)

# --- Paths and config ---
ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(ROOT / 'config.yml', 'r', encoding='utf-8'))

# --- Read raw deals ---
raw = read_json(str(ROOT / 'data' / 'deals_raw.json'), [])

# --- Categorise deals if missing category ---
for d in raw:
    if not d.get('category'):
        d['category'] = categorise(d.get('title', ''), CFG['site']['categories'])

# --- Apply filters and sort ---
curated = [d for d in raw if pass_filters(d, CFG)]
curated.sort(key=score_deal, reverse=True)

# --- Add affiliate tags to Amazon URLs ---
for d in curated:
    if "url" in d and d["url"]:
        d["url"] = add_affiliate_tag(d["url"])

# --- Write curated data ---
write_json(str(ROOT / 'data' / 'deals_curated.json'), curated)
print(f"Curated {len(curated)} deals → data/deals_curated.json")
