#!/usr/bin/env python3
"""WHATIF production health and SEO audit. Read only."""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
base="https://discoverwhatif.com"
errors=[]
def fetch(path):
    request=urllib.request.Request(base+path,headers={"User-Agent":"WHATIFSiteAudit/1.0"})
    with urllib.request.urlopen(request,timeout=20) as response:
        if response.status!=200: raise ValueError("HTTP "+str(response.status))
        return response.read()
for path in ("/","/robots.txt","/sitemap.xml","/tools.json","/analytics.js","/analytics-config.js"):
    try:
        content=fetch(path)
        if not content: raise ValueError("empty response")
        globals()["result_"+path.replace("/","_").replace(".","_")]=content
        print("OK",path)
    except Exception as exc: errors.append(path+": "+str(exc))
try:
    sitemap=ET.fromstring(fetch("/sitemap.xml"))
    urls=[node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    for url in urls:
        parsed=urlparse(url)
        if parsed.netloc!="discoverwhatif.com": errors.append("External sitemap entry: "+url)
        else:
            try: fetch(parsed.path or "/");print("OK sitemap page",parsed.path or "/")
            except Exception as exc: errors.append(url+": "+str(exc))
except Exception as exc: errors.append("Sitemap validation: "+str(exc))
try:
    tools=json.loads(fetch("/tools.json"))
    names=set()
    if not tools: errors.append("Empty tools directory")
    for tool in tools:
        name=tool.get("name")
        if not name or name in names: errors.append("Missing or duplicate tool: "+str(name))
        names.add(name)
        if urlparse(tool.get("url","")).scheme!="https": errors.append("Non-HTTPS tool URL: "+str(name))
    print("Validated",len(tools),"directory listings")
except Exception as exc: errors.append("Directory validation: "+str(exc))
for issue in errors: print("ERROR:",issue)
if errors: sys.exit(1)
print("WHATIF health and SEO audit passed.")
