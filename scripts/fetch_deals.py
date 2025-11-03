import os, json, yaml
from pathlib import Path
from .utils import write_json
from .merchants import mock_local, awin, amazon, ebay

ADAPTERS = {
    'mock_local': mock_local,
    'awin': awin,
    'amazon': amazon,
    'ebay': ebay,
}

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(ROOT / 'config.yml', 'r', encoding='utf-8'))

all_deals = []
for m in CFG['merchants']:
    if not m.get('enabled'):
        continue
    name = m['name']
    adapter = ADAPTERS.get(name)
    if not adapter:
        continue
    deals = adapter.fetch(CFG)
    all_deals.extend(deals)

write_json(str(ROOT / 'data' / 'deals_raw.json'), all_deals)
print(f"Fetched {len(all_deals)} deals → data/deals_raw.json")
