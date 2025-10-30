import json, yaml
from pathlib import Path
from utils import read_json, write_json, pass_filters, score_deal, categorise

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(ROOT / 'config.yml', 'r', encoding='utf-8'))

raw = read_json(str(ROOT / 'data' / 'deals_raw.json'), [])

for d in raw:
    if not d.get('category'):
        d['category'] = categorise(d.get('title',''), CFG['site']['categories'])

curated = [d for d in raw if pass_filters(d, CFG)]
curated.sort(key=score_deal, reverse=True)

write_json(str(ROOT / 'data' / 'deals_curated.json'), curated)
print(f"Curated {len(curated)} deals → data/deals_curated.json")
