# WHAT IF technical setup — completed October 16, 2026

Website: https://discoverwhatif.com/
Repository: https://github.com/rawedgedeals-alt/EdgeTools
Vercel production project: edgetools-7wus (prj_H1UMNPYDdmgVz05aZgEdqPklXqpO)

## Live changes

- All 20 software listings are included in the initial homepage HTML.
- Filtering, searching and sorting work, and approved affiliate links retain sponsored labels.
- Directory controls initialize from the HTML listings and can continue if live JSON updates fail.
- Improved homepage title/description, privacy-page description and factual WebSite structured data.
- Published shared GA4 tracking on the homepage, comparison guide and privacy page.
- Analytics consent prompt and footer preferences. Google tag does not load until consent; preview/local hosts are excluded.
- No free-text directory searches, email destinations or outbound query strings are included in the custom events.
- Updated privacy disclosures. Technical documentation and test scripts are excluded from deployments.

## Separate WHAT IF Google Analytics setup

- Account: WHAT IF (412308931)
- Property: WHAT IF — discoverwhatif.com (559328973)
- Reporting timezone: Chicago / America/Chicago, verified in Property details.
- Currency: USD.
- Web stream: WHAT IF website (16140618347), https://discoverwhatif.com
- Public measurement ID: G-SK9YZ6BR8F
- User approved and Google accepted the Analytics Terms of Service and Data Processing Terms.
- Optional account data-sharing choices disabled during creation; tag disables Google Signals and advertising personalization.
- Enhanced Measurement: history page views, automatic outbound clicks, site search and form interactions disabled. Page loads, scrolls, video engagement and file downloads remain enabled.
- Search Console domain discoverwhatif.com linked successfully to this web stream; its query and organic-search reports are available in Analytics navigation.
- Registered event-scoped custom dimensions: Tool name (tool_name), Tool category (category), Provider domain (provider_domain), Placement (placement).

## Verification

Production deployment READY at commit d2c78caaeb275231ef40e2467dd6ab19cada0fe2. SEO changes were merged in PR https://github.com/rawedgedeals-alt/EdgeTools/pull/1.

JavaScript tests passed for production host restrictions, consent, withdrawal, safe attribution/outbound parameters and no duplicate page-view initialization. Static checks passed for 20 cards, one h1/canonical per page, unique IDs and sitemap targets.

Live browser: AI filter shows 3 of 20; Shopify search shows 1 of 20; descending sort starts with Zapier; Shopify affiliate link uses sponsored noopener noreferrer. Google tag count was 0 before consent, 0 after declining, and 1 after allowing analytics.

GA4 Realtime confirmed our single test browser: one page_view, one tool_click, two directory_filter events, plus first_visit, session_start and scroll. This is setup test traffic, not proof of organic audience growth. Do not report it to advertisers as acquired traffic.

## Google indexing

- Homepage and public pages HTTP 200; nonexistent page 404.
- HTTP and www resolve to https://discoverwhatif.com/.
- robots.txt allows crawling and references the correct sitemap.
- Sitemap status in authenticated Search Console: Success, three discovered pages.
- Homepage indexed status at audit: Discovered — currently not indexed; no last crawl yet.
- Live Google inspection: page is available to Google and can be indexed.
- Indexing request submitted and confirmed. Repeated submissions do not improve its queue position. Indexing/rankings are not guaranteed.
- Aggregate Search Console reports were processing at setup. Standard GA4 reports and custom dimensions can take time to populate.

## Reading the traffic baseline

Use GA4 acquisition reports to compare source/medium and campaign traffic, engagement, and provider-link clicks. Use campaign links with utm_source, utm_medium and utm_campaign values that contain no personal information. Directory filter/search actions must not be counted as additional pages. Outbound clicks are referrals, not confirmed sales or affiliate revenue.

Analytics covers consenting, measurable browsers/devices; blockers and consent choices mean it is not an exact count of people. Earlier visits cannot be reconstructed by this installation. Use Search Console queries and landing-page impressions, once available, to choose useful new software comparisons and guides.

Scope held throughout: WHAT IF only. No RawEdge website, repository, analytics property or DNS settings were modified. No DNS changes were needed.
