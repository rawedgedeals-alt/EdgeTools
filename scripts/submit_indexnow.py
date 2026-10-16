#!/usr/bin/env python3
"""Notify IndexNow about explicitly selected, already published WHAT IF URLs."""
import argparse
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
HOST = "discoverwhatif.com"
ORIGIN = "https://" + HOST

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="Changed URLs from the WHAT IF sitemap")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    allowed = {e.text for e in ET.parse(ROOT / "sitemap.xml").iter()
               if e.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"}
    urls = list(dict.fromkeys(args.urls))
    if any(u not in allowed for u in urls):
        parser.error("Only explicit URLs from the WHAT IF sitemap may be submitted")
    keys = [p for p in ROOT.glob("*.txt") if re.fullmatch(r"[a-f0-9]{32}\.txt", p.name)]
    if len(keys) != 1:
        parser.error("Expected one IndexNow key file")
    key = keys[0].read_text().strip()
    if keys[0].stem != key:
        parser.error("Key content does not match filename")
    key_url = ORIGIN + "/" + keys[0].name
    if args.dry_run:
        print(json.dumps({"dryRun": True, "host": HOST, "urls": urls}, indent=2))
        return
    with urlopen(key_url, timeout=30) as response:
        if response.status != 200 or response.read().decode().strip() != key:
            raise SystemExit("Live ownership key is not ready; no URLs submitted")
    for url in urls:
        with urlopen(url, timeout=30) as response:
            if response.status != 200 or response.geturl() != url:
                raise SystemExit("URL is not published at its canonical address: " + url)
    payload = {"host": HOST, "key": key, "keyLocation": key_url, "urlList": urls}
    request = Request("https://api.indexnow.org/indexnow",
                      data=json.dumps(payload).encode(),
                      headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urlopen(request, timeout=30) as response:
            status = response.status
            response.read()
    except HTTPError as exc:
        raise SystemExit("IndexNow rejected submission: HTTP " + str(exc.code))
    if status not in (200, 202):
        raise SystemExit("Unexpected IndexNow response: HTTP " + str(status))
    print(json.dumps({"status": status, "urls": urls,
                      "result": "received" if status == 200 else "received; key validation pending",
                      "note": "Receipt does not guarantee crawling, indexing or ranking"}, indent=2))

if __name__ == "__main__":
    main()
