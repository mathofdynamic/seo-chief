# Site Audit and Technical SEO

## 1. Discover the real site

Use multiple sources; no single source is complete.

Inspect:
- framework/router/file routes;
- static and dynamic routes;
- sitemap(s);
- internal `<a href>` graph;
- canonical targets;
- redirects;
- CMS/database content when accessible;
- localization routes;
- production domain;
- logs/Search Console when available.

Flag:
- orphan routes;
- URLs in sitemap but not reachable;
- routes in code but not production;
- production pages absent from the repository inventory;
- duplicate/parameter variants.

## 2. Canonical Page Inventory

Recommended fields:

```text
url
final_url
page_type
purpose
status
indexability_decision
indexability_reason
canonical
robots_meta
x_robots_tag
robots_txt_access
language
locale
hreflang_set
rendering_mode
title
meta_description
h1
structured_data_types
sitemap_included
inlinks
outlinks
depth
primary_entity
target_intent
keyword_cluster
content_quality_flags
seo_findings
aeo_findings
geo_findings
severity
automation_class
validation_state
```

## 3. Indexability decision model

Choose intentionally:

- `index-follow`: unique public content with meaningful search/user value.
- `noindex-follow`: public utility/navigation content with no standalone search value.
- `noindex-nofollow`: rarely needed; use only with a clear reason.
- `robots-disallow`: crawl-control for sections that should not be fetched; not a de-index command.
- `canonicalize`: duplicate/near-duplicate URL where another URL is the preferred representative.
- `redirect`: content moved to a genuine replacement.
- `404`: resource absent with no replacement.
- `410`: intentionally removed resource where “gone” semantics are appropriate.
- `auth-protected`: private/account/admin content.

Typical defaults are in `page-types.md`; they are not substitutes for site-specific judgment.

### Controls are not interchangeable

- `robots.txt`: controls crawling, not guaranteed de-indexing.
- `meta robots` / `X-Robots-Tag`: indexing/snippet controls when a crawler can fetch the resource.
- canonical: consolidation hint for duplicates, not a replacement for access control.
- authentication: actual privacy/security control.
- redirect: routing/migration signal, not a generic duplicate-content bandage.

## 4. Crawlability

Check:
- valid root robots.txt;
- sitemap declaration where appropriate;
- important pages reachable with crawlable links;
- no infinite calendars/filter traps;
- bounded faceted navigation;
- no broken internal links;
- no redirect loops;
- flatten avoidable redirect chains;
- correct 404/410 semantics;
- no soft-404 template returning 200;
- expected handling of URL parameters;
- lower/upper-case and trailing-slash consistency;
- preferred HTTPS host.

Do not invent redirects. A deleted URL without a relevant replacement should not be sent to the homepage merely to preserve “SEO value.”

## 5. Sitemaps

A sitemap should contain canonical, intended-to-index URLs that return successful status codes.

Check:
- XML validity;
- sitemap index when scale requires it;
- accurate `lastmod` only when materially known;
- no noindex/redirect/4xx URLs;
- language/image/video/news extensions only when useful;
- automatic generation from a reliable source of truth;
- live file matches repository intent.

Do not fake `lastmod` on every build.

## 6. Canonicalization

Check:
- intended indexable pages have a coherent canonical policy;
- canonical does not point to a noindex/error/redirect URL;
- internal links and sitemap align with the preferred URL;
- parameter, protocol, host, trailing-slash, and case variants are consistent;
- hreflang references canonical equivalents.

Changing canonical targets across many pages is a high-impact change; use the safety matrix.

## 7. Rendering and JavaScript

Detect:
- SSR, SSG, ISR, server components, CSR/SPA, hydration model;
- whether critical text and metadata exist in initial HTML;
- whether content appears only after client execution;
- blocked scripts or resources;
- hydration mismatches;
- route payloads crawlers may not receive.

For key indexable pages, prefer robust server/static delivery of:
- title/meta/canonical;
- main heading;
- primary visible content;
- structured data;
- critical navigation.

Google can render JavaScript, but do not assume every search/AI crawler executes the same JS pipeline.

## 8. HTTP/CDN/WAF

Verify production:
- 200/3xx/4xx/5xx correctness;
- redirect behavior;
- canonical and robots headers;
- cache behavior;
- compression;
- CDN variants;
- rate limits;
- geo blocks;
- CAPTCHA/challenge behavior;
- bot-management rules.

Robots intent is irrelevant if the WAF returns 403/challenge pages to legitimate crawlers. Verify actual access and, where supported, published IP ownership rather than trusting user-agent strings alone.

## 9. Structured data

Prefer JSON-LD unless the project already uses another valid approach.

Rules:
- markup must match visible, truthful content;
- choose schema by page/entity, not by desired rich result;
- Schema.org validity does not imply Google/Bing presentation support;
- verify current search-engine support before promising a rich result;
- never invent reviews, ratings, prices, author identities, addresses, job details, or offers;
- validate syntax and required/recommended properties for the current platform feature.

## 10. Internal architecture

Audit:
- primary navigation;
- contextual links;
- breadcrumbs;
- hub/pillar relationships;
- related content;
- orphan pages;
- excessive depth;
- anchor clarity;
- overlinking/sitewide boilerplate.

Automated link proposals must be topically and contextually relevant. Do not insert exact-match anchors mechanically.

## 11. Multilingual / international

Inspect architecture before changing it.

Check:
- valid HTML `lang`;
- distinct localized URLs where intended;
- hreflang reciprocity;
- `x-default` where appropriate;
- canonical/hreflang compatibility;
- translated titles/descriptions/content;
- localized schema-visible strings;
- server behavior and auto-redirects;
- RTL correctness for Persian/Arabic;
- mixed-language accidental pages.

Do not canonicalize translated pages to the source language if they are intended as separate localized pages.

## 12. Images

Check:
- meaningful alt for informative images;
- empty alt for decorative images;
- dimensions/aspect ratio to reduce layout shift;
- responsive `srcset`/sizes where useful;
- sensible formats/compression;
- lazy loading away from the LCP image;
- priority/preload only when justified;
- descriptive surrounding context/captions when useful;
- crawlable image URLs;
- Open Graph image;
- image sitemap only when it materially improves discovery.

Alt text is primarily accessibility text. Do not stuff keywords into it.

## 13. Video

For important video pages check:
- crawlable dedicated page when appropriate;
- visible title/description;
- thumbnail;
- transcript/captions;
- `VideoObject` only when truthful/applicable;
- player load behavior;
- video sitemap when useful;
- text context so the page is understandable without watching.

## 14. Performance and page experience

Current Core Web Vitals must be verified against current web.dev documentation before hard enforcement. Measure field data separately from lab diagnostics.

Typical diagnostic areas:
- LCP;
- INP;
- CLS;
- TTFB;
- FCP;
- JS bundle/hydration cost;
- image sizing/loading;
- fonts;
- third-party scripts;
- caching/CDN;
- preload/preconnect misuse.

Do not claim a good Lighthouse score guarantees rankings. Relevance and content quality remain more important.

## 15. Mobile and accessibility

Check:
- mobile content parity;
- viewport;
- readable layout;
- usable navigation;
- intrusive interstitials;
- tap/interaction behavior;
- semantic landmarks;
- link vs button semantics;
- form labels;
- heading structure;
- keyboard basics;
- meaningful alt.

Do not claim every WCAG criterion is a ranking factor.
