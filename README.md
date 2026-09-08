# seo-chief

A repository-aware AI skill for complete **SEO + AEO + GEO** auditing, implementation, and validation.

`seo-chief` is designed for coding agents that can inspect both a web repository and its deployed domain. It treats classic search, answer extraction, and generative-search visibility as one evidence-gated system instead of three disconnected checklists.

## What it does

- discovers routes from code, sitemaps, internal links, CMS data, and production;
- builds a canonical Page Inventory;
- decides which pages should or should not be indexable;
- audits crawlability, rendering, canonicals, robots, sitemaps, redirects, hreflang, schema, media, mobile, and Core Web Vitals;
- evaluates every indexable page by page type and search intent;
- runs evidence-backed keyword research and detects cannibalization when relevant;
- separates AI **search/citation crawlers** from **training crawlers**;
- audits ChatGPT/Claude/Perplexity/Bing/Google generative-search accessibility without treating “GEO hacks” as established science;
- applies safe code changes using project-native patterns;
- requires approval for risky URL/indexability/content decisions;
- validates code and live production behavior;
- produces before/after evidence instead of an arbitrary SEO score.

## Invocation

```text
$seo-chief
```

Example:

```text
Use $seo-chief to audit and fully optimize this website for SEO, AEO, and GEO.
Inspect the repository and production domain, fix everything safe to fix, and give me one batch approval table for risky or keyword-targeted changes.
```

For a focused task:

```text
Use $seo-chief to audit this pricing page for crawlability, indexability, schema, search intent, AI citation readiness, and internal linking.
```

## Design principles

1. **Evidence before folklore.** Official, current platform documentation wins over generic SEO advice.
2. **Production truth matters.** Repository code is not proof of what crawlers actually receive.
3. **SEO is the foundation.** AEO/GEO extend crawlability, clarity, entity understanding, retrieval, and citation; they do not justify fake markup or formulaic copy.
4. **Search visibility and AI training consent are separate decisions.**
5. **Risk is asymmetric.** A missing meta description is not equivalent to accidentally noindexing a product catalog.
6. **No fabricated metrics or trust signals.**
7. **No forced mutation.** If a page is already correct, the skill should leave it alone.

## Repository layout

```text
seo-chief/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── aeo-geo.md
│   ├── evidence-policy.md
│   ├── evaluation-scenarios.md
│   ├── keyword-content.md
│   ├── page-types.md
│   ├── rule-schema.md
│   ├── safety-validation.md
│   ├── site-audit.md
│   └── source-registry.md
├── rules/
│   └── core-rules.json
├── scripts/
│   └── validate_rules.py
└── README.md
```

## Research basis

Version 1 is synthesized from a September 2026 multi-model research set covering Google Search/AI features, Bing/Copilot, ChatGPT Search, Perplexity, Claude search, Schema.org, Core Web Vitals, IndexNow, crawler controls, keyword research, page-type rules, structured data, content quality, automation safety, and production validation.

The research contains conflicting claims in fast-moving areas. The skill therefore does **not** treat the September 2026 snapshot as permanent truth. Time-sensitive Level-A rules must be re-verified against current first-party documentation before policy-sensitive implementation.

## Safety boundary

A broad request to “optimize everything” authorizes low-risk technical fixes and changes that can be mechanically validated. It does **not** automatically authorize:

- URL changes or mass redirects;
- noindex/robots blocks across meaningful content;
- page deletion / 410 decisions;
- legal or pricing changes;
- fabricated authors, reviews, ratings, statistics, testimonials, or credentials;
- competitor claims;
- keyword-targeted rewrites before the relevant page decision is approved.

Site-wide work uses a batch approval table to avoid a slow one-page-at-a-time workflow.

## Rule database

`rules/core-rules.json` contains machine-readable foundational rules. Each rule records:

- scope and applicability;
- check, expected state, fix, and validation;
- severity;
- automation class;
- SEO/AEO/GEO relevance;
- evidence level;
- source IDs;
- last verification date.

Validate it with:

```bash
python scripts/validate_rules.py
```

## License

No license has been selected yet.
