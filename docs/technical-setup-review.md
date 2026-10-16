# WHAT IF technical setup review — October 16, 2026

Target: https://discoverwhatif.com/
Repository: https://github.com/rawedgedeals-alt/EdgeTools
Branch: codex/whatif-seo-analytics-20261016

## Verified production and Google state

- Production homepage matches EdgeTools/main byte-for-byte (SHA256 6a6bc581c180bc616b159d679da6a0244054ae6292f0ebbdf721ef6874f633e8).
- Homepage, privacy page and Shopify/Webflow guide return HTTP 200. A nonexistent URL returns 404.
- HTTP and www requests resolve to https://discoverwhatif.com/.
- robots.txt allows crawling and references the correct sitemap.
- sitemap.xml is valid XML and contains the three canonical public pages.
- Authenticated Google Search Console domain property: discoverwhatif.com.
- Search Console sitemap status: Success; three discovered pages; read October 16, 2026.
- Homepage Google index status: Discovered — currently not indexed; no last crawl yet.
- Live inspection: URL is available to Google; page can be indexed.
- Submitted homepage indexing request; Google confirmed it was added to the priority crawl queue. This does not guarantee indexing or placement.
- Aggregate indexing/performance reports are still processing; no reliable traffic baseline yet.
- No GA4 tag was present in the audited production pages.

## Prepared code, awaiting production approval

- All 20 directory listings included in the initial HTML, retaining client-side filtering and sorting.
- Existing listings remain if live directory updates fail.
- Search-focused homepage title and description; factual WebSite structured data; privacy page description.
- Shared GA4 integration on all three pages. Measurement ID intentionally empty until a separate verified WHAT IF web stream exists.
- One initial page-view config; filter actions are not page views.
- Custom tool, sponsor, contact and category events; no free-text directory search collection.
- Optional analytics consent and footer preferences; no Google tag before consent, and a production hostname guard to exclude previews/local tests.
- Updated privacy disclosures and activation instructions.

Validation: JavaScript syntax checks; 20 static cards; one h1 and canonical per page; no duplicate element IDs; sitemap targets exist; tests cover production guard, accept/decline/withdrawal, no duplicate page-view initialization, safe attribution and outbound event parameters.

Not yet validated: real Google event receipt in Realtime/DebugView, visual browser QA of changed pages, or production deployment. Changes are local and not published.

## Account setup and access limits

Secure Google sign-in succeeded. Only the existing RawEdge analytics account/property was listed. It was not modified or reused.

A separate WHAT IF account creation form was prepared with property name “WHAT IF — discoverwhatif.com”, USD, small business, Computers & Electronics, optional account data-sharing choices off. No account/property was created; no Google agreement was accepted.

Planned report timezone: America/Chicago (Central time). Automatic approval review rejected selecting this timezone as unapproved, and then rejected proceeding with account creation because the form retained the default Los Angeles timezone. Explicit timezone approval is required before completing this setup. Google may also present terms requiring separate action-time approval.

Vercel returned edgetools and edgetools-7wus projects, but detailed scoped reads returned 403 for raw-edge. Neither project has been confirmed as the production domain owner. No Vercel CLI was installed locally. No Vercel settings were changed.

An automatic approval review rejected a branch push, classifying EdgeTools as the separate RawEdge repository. The later production-to-repository byte comparison and the repository README confirm WHAT IF's identity, but no retry or remote mutation was attempted after that rejection. Approval is requested specifically for rawedgedeals-alt/EdgeTools; all RAWEDGE-named repositories remain excluded.

## Next authorized sequence after approvals

1. Confirm Central report timezone and complete the separate WHAT IF GA4 account/property. Obtain approval at any actual Google agreement acceptance step.
2. Create one web stream for https://discoverwhatif.com/; disable automatic outbound clicks, history page views and site search; keep advertising features off.
3. Fill analytics-config.js with that stream's actual G- ID. Link the WHAT IF Search Console property.
4. Obtain/restore Vercel project access, confirm the project owning discoverwhatif.com, and verify branch deployment behavior before publishing.
5. Upload the prepared WHAT IF branch, review the diff/preview, publish only with user approval, then verify actual GA4 event receipt and live canonical/sitemap behavior.
6. Build the traffic baseline using acquisition sources and outbound tool clicks. Expand useful software guides based on actual search queries once Search Console data arrives.

No DNS changes are currently needed or proposed. RawEdge's website, repository, analytics property and DNS were not changed.

## Approval update

The user approved uploading/publishing the WHAT IF changes to rawedgedeals-alt/EdgeTools and using America/Chicago on October 16, 2026. Central time has now been selected. The GA4 form is paused at Google Analytics Terms of Service Agreement pending action-time approval. No new GA4 account/property exists yet and tracking remains disabled.

Vercel unscoped project reads and domain listing now confirm edgetools-7wus (prj_H1UMNPYDdmgVz05aZgEdqPklXqpO) owns discoverwhatif.com and its www redirect, both verified. No DNS edits are needed. Git CLI upload failed for missing credentials; connected GitHub tools will be used for the approved repository upload.
