import os, re, json, time, math, logging, datetime as dt
from typing import List, Dict, Any
from slugify import slugify

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

ISO = '%Y-%m-%dT%H:%M:%SZ'

def now_utc() -> str:
    return dt.datetime.utcnow().strftime(ISO)

def read_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def pct_off(price: float, list_price: float) -> int:
    if not list_price or list_price <= 0:
        return 0
    return max(0, int(round((1 - (price / list_price)) * 100)))

def pass_filters(deal: Dict[str, Any], cfg: Dict[str, Any]) -> bool:
    if deal.get('price') is None:
        return False
    if deal['price'] > cfg['filters']['max_price']:
        return False
    if deal.get('list_price'):
        deal['discount_pct'] = pct_off(deal['price'], deal['list_price'])
    if deal.get('discount_pct', 0) < cfg['filters']['min_discount_pct']:
        return False
    title = (deal.get('title') or '').lower()
    for phrase in cfg['filters'].get('exclude_phrases', []):
        if phrase.lower() in title:
            return False
    return True

def score_deal(d):
    recency_boost = 0
    try:
        ts = dt.datetime.strptime(d.get('timestamp', now_utc()), ISO)
        age_h = (dt.datetime.utcnow() - ts).total_seconds() / 3600
        recency_boost = max(0, 24 - min(24, age_h)) / 24 * 5
    except Exception:
        pass
    reviews = (d.get('meta', {}) or {}).get('reviews', 0)
    review_boost = min(5, math.log1p(reviews))
        # Manual deals get a slight boost to ensure visibility
    if d.get("manual"):
        return 100 + d.get('discount_pct', 0) + recency_boost + review_boost
    # Normal deals score by discount, recency, and reviews
    return d.get('discount_pct', 0) + recency_boost + review_boost

def categorise(title: str, categories: List[Dict[str, Any]]):
    t = (title or '').lower()
    for c in categories:
        if any(k.lower() in t for k in c.get('keywords', [])):
            return c['slug']
    return 'other'

# --- Affiliate helpers -------------------------------------------------------

AFFILIATE_TAG = "techdealsuk0a-21"


def add_affiliate_tag(url: str) -> str:
    """
    If the URL is an Amazon link, append our affiliate tag.
    Otherwise, return the URL unchanged.
    """
    if not url:
        return url

    # Only touch Amazon links
    if "amazon." not in url.lower():
        return url

    # Don't double-tag
    if "tag=" in url.lower():
        return url

    # If there's already a query string, use & otherwise use ?
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}tag={AFFILIATE_TAG}"
