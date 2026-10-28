#!/usr/bin/env python3
"""Validate legacy research inventory. No third-party cards belong on the WHATIF homepage.

The WHATIF storefront now promotes owned products first. tools.json remains as
an editorial research archive and for link monitoring only, not a paid ranking
system or an automatic promotional listing feed.
"""
import json
import pathlib
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]

def render():
    path = ROOT / "tools.json"
    providers = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(providers, list):
        raise ValueError("Expected a provider list")
    for i, provider in enumerate(providers, 1):
        if not isinstance(provider, dict) or not str(provider.get("name", "")).strip():
            raise ValueError(f"Missing provider name at item {i}")
        u = urlparse(str(provider.get("url", "")))
        if u.scheme != "https" or not u.hostname:
            raise ValueError(f"Provider must use HTTPS at item {i}")
    print(f"Validated {len(providers)} legacy research entries; no external listings published to homepage.")

if __name__ == "__main__":
    render()
