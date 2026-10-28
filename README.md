# WHATIF — Our Tools, Your Ideas

Website: https://discoverwhatif.com/

## Mission

**What if technology could be simple? Now IT is. With WHAT IF.**
**For those of us who don't speak code.**

WHATIF is moving from a third-party software directory toward a first-party,
accessible software platform. The priority is useful WHATIF-owned software and
a consistent easy experience—not sending visitors to a grid of free vendor ads.

## First-party tools built

- `website-starter.html`: three-question website builder, instant preview,
  downloadable standalone HTML website, three selectable cinematic designs.
  **Does not publish/host websites**, accept payments, or provide customer accounts.
- `software-stack-planner.html`: private browser-local subscription audit,
  recurring cost estimates, category overlap hints and CSV export.
- `software-cost-calculator.html`: basic subscription and first-year cost estimate.
- `small-business-software-stack-checklist.html`: educational first-party guide.

The Edge Motion video studio exists as an offline prototype but is **not yet
integrated into discoverwhatif.com**. The unified marketing workspace, site
monitor, and account-based product platform are **planned, not available**.

## External brands and advertising

The homepage does **not** display the 20 legacy vendor directory cards. Data
in `tools.json` and `affiliate-links.json` remains for editorial research and
past approved relationships; neither file powers an external-brand grid on the
new homepage. `directory.js` is legacy code not loaded on the homepage.
`scripts/render_directory.py` now validates the legacy inventory instead of
modifying `index.html`.

Independent educational comparisons may name products when relevant. They do
not imply paid affiliation or endorsements. Outside companies must arrange
paid, clearly labeled promotional placement to get an ad feature.
`ads.json` contains three optional advertising slots, all inactive by default.
`ads.js` renders only active sponsor campaigns and uses
`rel="sponsored noopener noreferrer"` for advertiser links. **No empty ad
billboards appear**.

The `advertise.html` page proposes sponsor packages but does not process
payments. No sponsor is active or implied by having a prospect entry.

## Search / privacy / analytics

The main SEO content stays accessible through independent guides. `sitemap.xml`
lists the first-party tool pages and editorial articles. Analytics runs via
`analytics-config.js` + `analytics.js` only after explicit consent on the
production domain. Analytics is not a complete visitor census.

## Release process

This redesign is on a feature branch until reviewed and merged. Test the
responsive homepage, interactive builder, downloaded files, sponsor gating
and consent behavior on a Vercel preview before publishing to production.
Do not change DNS or RawEdge while working on WHATIF.
