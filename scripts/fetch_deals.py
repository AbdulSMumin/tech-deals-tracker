import os, json, yaml
from pathlib import Path
from scripts.utils import write_json, read_json
from .merchants import mock_local, awin, amazon, ebay

ADAPTERS = {
    'mock_local': mock_local,
    'awin': awin,
    'amazon': amazon,
    'ebay': ebay,
}

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(ROOT / 'config.yml', 'r', encoding='utf-8'))

def main():
    raw_path = ROOT / 'data' / 'deals_raw.json'

    # 1) Load any existing deals
    existing = read_json(str(raw_path), [])

    # 2) Preserve any deals you've marked as manual
    manual_deals = [d for d in existing if d.get('manual')]

    # 3) Fetch from all enabled merchants (mock_local / awin / amazon / ebay)
    fetched_deals = []
    for m in CFG['merchants']:
        if not m.get('enabled'):
            continue
        name = m['name']
        adapter = ADAPTERS.get(name)
        if not adapter:
            continue
        deals = adapter.fetch(CFG)
        fetched_deals.extend(deals)

    # 4) Combine manual + fetched
    all_deals = manual_deals + fetched_deals

    write_json(str(raw_path), all_deals)
    print(f"Fetched {len(all_deals)} deals → data/deals_raw.json")

if __name__ == '__main__':
    main()
