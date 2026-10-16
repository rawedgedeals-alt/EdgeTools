# WHATIF — Software Discovery

Website: https://discoverwhatif.com/

Static WHATIF directory. `tools.json` contains provider listings and category metadata. Once an affiliate account is approved, add its matching name and official HTTPS link to `affiliate-links.json` with `approved: true`; the directory will use that link with a visible affiliate disclosure. No unapproved tracking links are used.

Sponsored campaigns are controlled in `ads.json` (slots: hero, mid, bottom). Activate only real campaigns. `ads.js` shows clearly marked advertising placeholders otherwise.

The existing daily GitHub link monitor checks basic provider URL reachability, not pricing, commissions or performance.

## Search visibility

After updating `tools.json`, run `python3 scripts/render_directory.py` and commit
`index.html` too. The delivered HTML includes every tool, so the directory works
without JavaScript. `directory.js` adds filtering, sorting and approved affiliate
links. If its live data request fails, the existing listings remain available.

## Analytics activation

Set `measurementId` in `analytics-config.js` to the verified WHAT IF GA4 web
stream ID. An empty ID disables tracking. Do not use a RawEdge property or ID.
Analytics loads only on `discoverwhatif.com` and only after consent; previews,
local development and visitors declining analytics do not send events.

One GA4 `config` call sends the initial page view. Do not add a second Google
tag, GTM page-view tag, or manual page-view call. In Enhanced Measurement,
disable automatic outbound clicks, history-change page views and site-search collection: filters aren't
pages and free-text directory searches should not be collected. Generic GA4
outbound `click` events and `tool_click` are different metrics, not additive
conversion totals. Leave Google Signals and advertising features disabled.

Custom events: `tool_click` (tool name, category, destination hostname, affiliate
flag), `sponsor_click` (placement, destination hostname), `contact_click`
(placement only), and `directory_filter` (category only). No free-text searches,
email destinations, or outbound URL query strings are sent by these events.
Use UTM campaign links without personal information to distinguish traffic
sources. GA4 users represent measured browsers/devices, not a count of people.

Before production approval, verify the WHAT IF property, ID, report timezone,
web stream URL, and Search Console association. After an approved deployment,
accept analytics in a fresh visit and verify one `page_view` and one
`tool_click` in Realtime/DebugView; check decline and preferences withdrawal.
Data starts after activation and can't reconstruct earlier visits. Consent and
browser blocking mean analytics is not a complete visitor census.
