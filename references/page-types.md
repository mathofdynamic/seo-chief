# Page-Type Playbooks

Defaults are starting points, not automatic directives. Site purpose and content quality can override them.

| Page type | Typical indexability | Main schema candidates | Main risks |
|---|---|---|---|
| Homepage | index | Organization, WebSite, WebPage | vague positioning, weak entity clarity |
| Product/SaaS | index | Product, SoftwareApplication, WebApplication, Offer when truthful | marketing-only copy, invented claims |
| Feature | index if substantively distinct | WebPage/Product-related entity | thin near-duplicate pages |
| Solution/use case | index if genuinely specific | Service/WebPage | templated industry doorway pages |
| Pricing | usually index | Product/Offer when current | stale/invented pricing |
| Comparison/alternative | index if original/fair | WebPage/ItemList as appropriate | fabricated competitor claims, scaled pages |
| Integration | index if real integration depth | SoftwareApplication/Product/WebPage | templated pages with noun swaps |
| Documentation/API | index | WebPage/TechArticle-like semantics where suitable | client-only rendering, stale versions |
| Blog index | usually index | CollectionPage | thin taxonomy duplication |
| Article/tutorial | index | Article/BlogPosting | commodity copy, fake author/freshness |
| Case study | index | Article/WebPage | invented outcomes/testimonials |
| Changelog | index if substantive | WebPage/CollectionPage | fake dates, thin entries |
| About | index | AboutPage, Organization, Person where genuine | fabricated credentials |
| Team/author | index when useful | ProfilePage, Person | fake identities/bios |
| Contact | usually index | ContactPage, Organization/LocalBusiness if relevant | inconsistent entity data |
| Careers/job | index while active | JobPosting | stale/expired jobs, missing required facts |
| Local business | index | LocalBusiness subtype | inconsistent NAP/hours |
| Ecommerce category | index if useful | CollectionPage/ItemList | faceted duplication |
| Ecommerce product | index if available/useful | Product, Offer, Review only when real | duplicate manufacturer copy, fake ratings |
| Search/filter/facet | usually noindex or controlled | none usually | crawl traps/index bloat |
| Login/signup/reset | noindex/private | none | accidental indexability |
| Dashboard/account/admin | auth-protected | none | privacy exposure |
| Checkout/cart | usually noindex | transaction-specific | index bloat/private data |
| Legal/privacy/terms | case-by-case, usually crawlable | WebPage | unauthorized legal edits |
| Staging/preview | never public-indexable | none | leaks |

## Homepage

Required:
- clear canonical organization/product naming;
- concise value proposition based on real product facts;
- links to primary products/features/solutions/docs;
- Organization/WebSite schema when truthful;
- trust/contact/about routes where relevant.

AEO/GEO:
- directly state what the company/product is and who it serves;
- avoid hero copy that is only adjectives.

Automation:
- technical metadata/schema can be auto-with-validation when sourced from visible facts;
- positioning rewrites require approved content intent.

## Product / SaaS

Required:
- what it is;
- real capabilities;
- audience/use cases;
- differentiators supported by evidence;
- pricing link or truthful pricing if public;
- docs/support links where useful.

Schema:
- choose Product/SoftwareApplication/WebApplication based on actual semantics;
- Offer only with real current commercial data.

Never invent features, compatibility, users, results, prices, reviews, or ratings.

## Feature

Index only when the page adds meaningful, unique detail.

Flag:
- near-duplicate feature pages;
- keyword-swapped templates;
- pages that should be one section of a stronger product page.

## Solution / use case

Require genuine audience/problem-specific content. A page that only replaces “healthcare” with “finance” across the same template is a scaled-content risk.

## Pricing

Treat prices, discounts, currencies, billing periods, free-trial terms, and availability as human/business facts.

Never auto-change them.

## Comparison / alternatives

High-risk content category.

Require:
- sourced current competitor facts;
- fair comparison criteria;
- clear update date;
- real product knowledge.

Never mass-generate competitor claims.

## Integration

Require real technical integration detail:
- supported actions/data;
- setup;
- limitations;
- version/dependency context;
- docs links.

## Documentation / API

Prioritize:
- server/static rendering;
- stable URLs;
- versioning;
- code examples;
- error behavior;
- navigation/hierarchy;
- last-updated accuracy;
- no broken anchors;
- canonical handling.

Docs can be high-value sources for AI retrieval; correctness matters more than marketing language.

## Article / guide / tutorial

Before creation:
- unique reader problem;
- intent;
- overlap/cannibalization check;
- information gain;
- source requirements;
- outline;
- internal links;
- CTA;
- freshness risk.

Use Article/BlogPosting only when appropriate. Use genuine author/date information.

## Case study

Never fabricate:
- customer identity;
- quotes;
- metrics;
- screenshots;
- outcomes.

If evidence is missing, leave a clearly identified content gap rather than generating plausible numbers.

## About / team / contact

Use these to reinforce entity clarity and trust, not to manufacture E-E-A-T.

Only create Person data for real people.

## Local business

Verify:
- name;
- address;
- phone;
- hours;
- geo/service area;
- business category;
- sameAs profiles.

Do not infer missing NAP data.

## Ecommerce

Category:
- control facets;
- useful category copy only if it adds user value;
- breadcrumbs;
- crawlable product links.

Product:
- unique product data;
- availability and price accuracy;
- canonical variants;
- image quality;
- Product/Offer/Review only from real data.

## Search / filter / faceted navigation

Usually control indexability unless a facet is intentionally promoted into a unique landing page with clear value.

Do not create thousands of indexable parameter combinations.

## Auth / dashboard / checkout / admin

Prefer authentication and explicit privacy controls over relying on robots.txt.

## Legal

SEO Chief may audit metadata/indexability and flag issues. It must not substantively rewrite legal terms without explicit instruction and appropriate review.
