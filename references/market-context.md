# Market, Product, and Content Context

Use this reference before keyword mapping, page creation, comparison content, programmatic SEO, or material content rewrites.

## 1. Discover context before asking

Inspect the repository for existing business/marketing truth before asking the user to repeat it.

Likely sources include:
- `AGENTS.md`, `CLAUDE.md`, project READMEs and docs;
- `.agents/product-marketing.md`;
- `.claude/product-marketing.md`;
- `product-marketing-context.md`;
- product/brand/positioning docs;
- pricing/config/product catalogs;
- public About, Features, Pricing, Docs, Changelog and Contact pages;
- schema/entity data already maintained by the project;
- connected analytics/Search Console/CRM/support data when explicitly available.

Repository naming conventions are examples, not mandatory filenames. Search for equivalent project-owned context.

Ask only for facts that materially affect the work and cannot be established safely.

## 2. Source-of-truth hierarchy for business claims

Prefer, in order:
1. explicit current user instruction;
2. current project-owned structured data/config used by the product;
3. current project-owned product/marketing documentation;
4. current public product pages/docs;
5. connected first-party business systems when authorized;
6. current first-party vendor documentation for integrations/competitors;
7. reputable external sources.

When sources conflict, surface the conflict. Do not silently choose the more SEO-convenient claim.

Never infer or invent:
- pricing;
- customer counts;
- outcomes;
- certifications;
- compatibility;
- feature availability;
- addresses/hours;
- awards;
- competitor capabilities;
- legal/compliance status.

## 3. Customer-language evidence

Keyword research should not depend only on keyword tools. When available, mine first-party customer evidence for language and intent:
- sales-call questions;
- support tickets;
- onboarding questions;
- internal site search;
- CRM loss/win reasons;
- surveys;
- reviews supplied or legitimately accessible;
- product feedback;
- community questions;
- documentation searches.

Extract:
- repeated questions;
- jobs-to-be-done;
- pain language;
- objections;
- evaluation criteria;
- competitor mentions;
- implementation questions;
- terminology customers actually use.

Treat these as qualitative evidence. Do not invent frequency percentages when the dataset is incomplete.

## 4. Content opportunity model

For a proposed page/article, consider:
- user/business problem;
- search demand evidence;
- current first-party query evidence;
- product relevance;
- conversion relevance;
- SERP/result-type fit;
- information gain;
- evidence/data availability;
- maintenance cost/freshness risk;
- cannibalization;
- internal-link role;
- off-site distribution or citation potential when relevant.

Any weighted score is an internal prioritization tool, not a search-engine metric. Disclose the inputs and missing data.

## 5. Programmatic SEO data provenance

Before creating pages at scale, record where page-specific value comes from.

A useful provenance ladder is:
1. proprietary research/data;
2. product-derived data or functionality;
3. genuine user-generated/community data;
4. licensed data with redistribution rights;
5. maintained public/official data;
6. generic prose or variable substitution only.

The ladder is about defensibility and unique value, not an automatic ranking score.

Require a page-generation contract containing:

```text
page_pattern
user_intent
unique_data_fields
data_source
source_update_frequency
minimum_unique_value
quality_gate
indexation_gate
internal_link_source
canonical_policy
stale_data_behavior
owner
```

Do not generate/index a page merely because a row exists in a CSV.

## 6. Staged programmatic launches

For large page sets:
1. validate demand and page pattern;
2. ship a small representative cohort;
3. validate template quality, crawlability, rendering, uniqueness and conversion usefulness;
4. monitor indexation/crawl/search evidence when available;
5. expand only if the cohort remains useful and maintainable.

Do not use automatic `noindex` as a substitute for fixing a bad generation strategy. If a page has no durable user value, prefer not creating it.

## 7. Comparison and alternative page evidence

Comparison content must be useful even to a reader who does not choose the site owner's product.

Maintain a current evidence record per competitor:

```text
competitor
canonical_name
official_url
facts_checked_at
pricing_source
feature_sources
strengths
limitations
best_fit
not_best_fit
migration_notes
uncertainties
```

Rules:
- acknowledge competitor strengths when true;
- distinguish facts from opinion;
- use the same criteria across compared products;
- date volatile facts such as pricing/features;
- do not create fake weaknesses or self-serving scores;
- do not manufacture testimonials from switchers;
- centralize repeated competitor facts where possible so updates propagate consistently.

Comparison-page freshness is a maintenance obligation, not a reason to fake `dateModified`.

## 8. Site architecture as a graph, not a magic click count

Audit:
- orphan pages;
- crawl depth distribution;
- navigation zones;
- hubs/spokes;
- contextual cross-section links;
- important pages with weak inlinks;
- excessive boilerplate linking;
- URL hierarchy consistency;
- breadcrumb relationships.

Use business importance, user journeys, crawl evidence and information architecture to prioritize links. Do not enforce a universal `3-click rule` or a fixed links-per-1000-words quota.

## 9. External presence and authority

External sources may reveal where an audience or generative system encounters an entity, but they do not justify manufactured authority.

Legitimate recommendations may include:
- accurate third-party profiles;
- editorial coverage;
- original datasets/research;
- public tools;
- useful documentation;
- authentic community participation;
- videos/podcasts with accessible text layers;
- review-platform profile hygiene.

Never automate astroturfing, fake reviews, synthetic community mentions, link schemes, or Wikipedia manipulation.
