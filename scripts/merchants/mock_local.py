import os, json, random, datetime as dt
from ..utils import now_utc

SAMPLE = [
  {"title": "Logitech G203 Wired Gaming Mouse", "price": 18.99, "list_price": 29.99, "image": "https://images.example/g203.jpg", "meta": {"rating": 4.6, "reviews": 2789}},
  {"title": "Kingston NV2 500GB NVMe SSD", "price": 29.99, "list_price": 49.99, "image": "https://images.example/nv2.jpg", "meta": {"rating": 4.5, "reviews": 15421}},
  {"title": "HyperX Cloud Stinger 2", "price": 34.99, "list_price": 59.99, "image": "https://images.example/stinger2.jpg", "meta": {"rating": 4.4, "reviews": 9121}},
  {"title": "Corsair K55 RGB Keyboard", "price": 24.99, "list_price": 49.99, "image": "https://images.example/k55.jpg", "meta": {"rating": 4.3, "reviews": 11021}},
]

def fetch(config):
    out = []
    ts = now_utc()
    for i, s in enumerate(SAMPLE):
        out.append({
            "id": f"mock:{i}",
            "title": s["title"],
            "merchant": "mock",
            "url": "#",
            "price": s["price"],
            "list_price": s["list_price"],
            "discount_pct": None,
            "image": s["image"],
            "category": None,
            "timestamp": ts,
            "meta": s.get("meta", {}),
        })
    return out
