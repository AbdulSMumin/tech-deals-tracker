from pathlib import Path
import yaml
from .utils import read_json, write_json

ROOT = Path(__file__).resolve().parents[1]
CFG = yaml.safe_load(open(ROOT / 'config.yml', 'r', encoding='utf-8'))
curated = read_json(str(ROOT / 'data' / 'deals_curated.json'), [])

TOP = 10
write_json(str(ROOT / 'data' / 'email_digest.json'), curated[:TOP])
print("Digest created → data/email_digest.json")
