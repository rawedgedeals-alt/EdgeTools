#!/usr/bin/env python3
"""Publish only curated WHATIF evergreen articles that have reached their date.

No AI generation, no API keys, no paid services, no third-party promises.
Idempotent and safe to run unattended once a week.
"""
import datetime as dt
import html
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"content"/"evergreen-guides.json"
OUT=ROOT/"learn"
BASE="https://discoverwhatif.com"
CENTRAL=ZoneInfo("America/Chicago")
TODAY=dt.datetime.now(CENTRAL).date()
def escape(value):return html.escape(str(value),quote=True)
def valid_slug(value):return isinstance(value,str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",value) and len(value)<=80
def page(article):
    slug=article["slug"];url=f"{BASE}/learn/{slug}.html"
    desc=escape(article["summary"])
    sections="".join(f'<section><h2>{escape(s["heading"])}</h2>'+''.join(f'<p>{escape(p)}</p>' for p in s["paragraphs"])+'</section>' for s in article["sections"])
    metadata={"@context":"https://schema.org","@type":"Article","headline":article["title"],
       "description":article["summary"],"datePublished":article["publish_date"],
       "mainEntityOfPage":url,"publisher":{"@type":"Organization","name":"WHATIF","url":BASE}}
    schema=json.dumps(metadata).replace("<","\\u003c")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(article["title"])} | WHATIF</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="WHATIF">
<meta property="og:title" content="{escape(article["title"])}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="../guide.css">
<script src="../analytics-config.js" defer></script><script src="../analytics.js" defer></script>
<script type="application/ld+json">{schema}</script>
<style>article{{max-width:820px}}article p{{font-size:17px}}.return{{margin-top:45px;border:1px solid #26f3a077;border-radius:16px;padding:24px;background:#10251f}}.return a{{font-weight:800}}</style>
</head><body><header><a class="brand" href="../index.html">WHAT<span>IF?</span></a>
<nav><a href="../website-starter.html">BUILD</a> &nbsp; <a href="../software-stack-planner.html">PLAN</a> &nbsp; <a href="./index.html">LEARN</a></nav></header>
<main><article><p class="eyebrow">SIMPLE TECH · PRACTICAL GUIDES</p>
<h1>{escape(article["title"])}</h1><p class="intro">{escape(article["summary"])}</p>
<p class="meta">Published {escape(article["publish_date"])} · Independent educational guide</p>
{sections}
<section class="return"><h2>Your next step</h2><p>Try a free tool built by WHATIF. A downloaded website file is not a hosted website, and third-party prices or features can change.</p>
<a class="cta" href="../{escape(article["tool_path"])}">TRY THE FREE TOOL</a></section>
</article></main><footer>© WHATIF · <a href="../privacy.html">Privacy</a> · <a href="./index.html">More guides</a></footer></body></html>
"""
def listing(items):
    cards="\n".join(f'<div class="card"><span class="tag">{escape(a["publish_date"])} · GUIDE</span>'
          f'<h3>{escape(a["title"])}</h3><p>{escape(a["summary"])}</p>'
          f'<a href="{escape(a["slug"])}.html">READ GUIDE →</a></div>' for a in items)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Free Guides for People Who Don't Speak Code | WHATIF</title>
<meta name="description" content="Practical free WHATIF guides on simpler software choices, business websites and subscription costs.">
<link rel="canonical" href="{BASE}/learn/index.html"><link rel="stylesheet" href="../guide.css">
<script src="../analytics-config.js" defer></script><script src="../analytics.js" defer></script>
<style>.articles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:17px}}.card p{{min-height:88px}}</style></head>
<body><header><a class="brand" href="../index.html">WHAT<span>IF?</span></a><nav><a href="../index.html">HOME</a></nav></header>
<main><p class="eyebrow">WHAT IF TECHNOLOGY COULD BE SIMPLE?</p><h1>Tech, without the <span>headache.</span></h1>
<p class="intro">Free, independent guidance for people who don't speak code. Made for owners, creators and everyday problem-solvers.</p>
<div class="articles">{cards}</div><div class="panel"><h2>Tools you can actually use</h2>
<p>Try our free <a href="../website-starter.html">Website Starter</a>, <a href="../software-stack-planner.html">Stack Planner</a> or <a href="../software-cost-calculator.html">Cost Calculator</a>.</p>
</div></main><footer>© WHATIF · <a href="../privacy.html">Privacy</a></footer></body></html>
"""
def main():
    rows=json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(rows,list):raise ValueError("Expected array")
    chosen=[];seen=set()
    for a in rows:
        slug=a.get("slug")
        if not valid_slug(slug) or slug in seen:raise ValueError("Invalid or duplicate slug: "+str(slug))
        seen.add(slug)
        date=dt.date.fromisoformat(a["publish_date"])
        if not a.get("editorial_approved"):continue
        if date>TODAY:continue
        if a.get("tool_path") not in {"website-starter.html","software-stack-planner.html","software-cost-calculator.html"}:
            raise ValueError("Unapproved first-party tool path")
        if not a.get("sections") or not all(s.get("heading") and s.get("paragraphs") for s in a["sections"]):
            raise ValueError("Incomplete approved guide")
        chosen.append(a)
    chosen.sort(key=lambda a:a["publish_date"],reverse=True)
    if not chosen:
        print("No due approved WHATIF guides. No changes.")
        return
    OUT.mkdir(parents=True,exist_ok=True)
    for a in chosen:
        (OUT/(a["slug"]+".html")).write_text(page(a),encoding="utf-8")
    (OUT/"index.html").write_text(listing(chosen),encoding="utf-8")
    sitemap=ROOT/"sitemap.xml"
    old=sitemap.read_text(encoding="utf-8")
    urls=[f"{BASE}/learn/index.html"]+[f'{BASE}/learn/{a["slug"]}.html' for a in chosen]
    updates=''.join(f'\n<url><loc>{url}</loc></url>' for url in urls if f'<loc>{url}</loc>' not in old)
    if updates:
        if "</urlset>" not in old:raise ValueError("Cannot update sitemap")
        sitemap.write_text(old.replace("</urlset>",updates+"\n</urlset>"),encoding="utf-8")
    print(json.dumps({"published_approved_guides":len(chosen),"date_central":TODAY.isoformat(),"new_sitemap_urls":len([u for u in urls if f'<loc>{u}</loc>' not in old])}))
if __name__=="__main__":main()
