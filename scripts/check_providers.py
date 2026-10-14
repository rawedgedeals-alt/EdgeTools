#!/usr/bin/env python3
"""EdgeTools daily provider link monitor. Never fabricates prices, promotions or ratings."""
import json, pathlib, datetime, urllib.request, urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
items=json.loads((ROOT/"tools.json").read_text())
results=[]
for item in items:
    url=item.get("url","")
    status="unknown"
    if url.startswith("https://"):
        try:
            request=urllib.request.Request(url,headers={"User-Agent":"EdgeToolsLinkMonitor/1.0 (public website link verification)"},method="HEAD")
            with urllib.request.urlopen(request,timeout=12) as response:
                status="reachable" if response.status<400 else "review"
        except urllib.error.HTTPError as e:
            status="unknown" if e.code in (401,403,405,429) else "review"
        except Exception:
            status="unknown"
    results.append({"name":item["name"],"url":url,"link_status":status})
report={"last_checked_utc":datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),"note":"Automated link checks only. Unknown does not imply a provider is offline. No offer, price, or affiliate verification is claimed.","providers":results}
(ROOT/"monitor-status.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({"checked":len(results),"statuses":{x["name"]:x["link_status"] for x in results}}))
