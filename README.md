# WHATIF — Software Discovery

Website: https://discoverwhatif.com/

Static WHATIF directory. `tools.json` contains provider listings and category metadata. Once an affiliate account is approved, add its matching name and official HTTPS link to `affiliate-links.json` with `approved: true`; the directory will use that link with a visible affiliate disclosure. No unapproved tracking links are used.

Sponsored campaigns are controlled in `ads.json` (slots: hero, mid, bottom). Activate only real campaigns. `ads.js` shows clearly marked advertising placeholders otherwise.

The existing daily GitHub link monitor checks basic provider URL reachability, not pricing, commissions or performance.
