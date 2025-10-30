import os, requests
from ..utils import now_utc

BASE = "https://api.awin.com/advertisers/-/transactions"

def fetch(config):
    api_key = os.getenv('AWIN_API_KEY')
    if not api_key:
        return []
    # Placeholder to avoid accidental API calls. Replace with Awin product feed integration.
    return []
