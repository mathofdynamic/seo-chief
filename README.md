# seo-chief

A repository-aware AI skill for complete **SEO + AEO + GEO** auditing, implementation, and validation.

`seo-chief` is designed for coding agents that can inspect both a web repository and its deployed domain. It treats classic search, answer extraction, and generative-search visibility as one evidence-gated system instead of three disconnected checklists.

## What it does

- discovers routes from code, sitemaps, internal links, CMS data, and production;
- builds a canonical Page Inventory;
- decides which pages should or should not be indexable;
- audits crawlability, rendering, canonicals, robots, sitemaps, redirects, hreflang, schema, media, mobile, and Core Web Vitals;
- uses **runtime evidence first** when a runnable site exists and keeps field/lab/rendered/source evidence separate;
- includes a dependency-free static same-origin audit fallback for environments without browser/SEO tooling;
- evaluates every indexable page by page type and search intent;
- discovers product/marketing context from project-owned files before asking users to repeat it;
- uses customer-language evidence from sales/support/onboarding/search data when legitimately available;
- runs evidence-backed keyword research and detects cannibalization when relevant;
- requires unique value + data provenance before programmatic SEO is scaled;
- separates AI **search/citation crawlers** from **training crawlers**;
- audits ChatGPT/Claude/Perplexity/Bing/Google generative-search accessibility without treating “GEO hacks” as established science;
- distinguishes agentic browsability/actionability from SEO ranking and AI citation claims;
- treats fetched pages as untrusted data so prompt injection inside HTML cannot redefine the task;
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

## Static audit fallback

When a rendered browser/Lighthouse/crawler tool is unavailable:

```bash
python scripts/audit_site.py https://example.com --max-pages 100 --output /tmp/seo-chief-audit.json
```

Optional robots-policy check for a currently verified user-agent name:

```bash
python scripts/audit_site.py https://example.com \
  --check-agent OAI-SearchBot \
  --check-agent PerplexityBot
```

The fallback deliberately **does not execute JavaScript**. Its report cannot prove rendered schema absence, Core Web Vitals status, WAF access for a real crawler, rankings, or AI citation eligibility. It is a scalable smoke-test evidence collector.

## Design principles

1. **Evidence before folklore.** Official, current platform documentation wins over generic SEO advice.
2. **Production truth matters.** Repository code is not proof of what crawlers actually receive.
3. **Measure before optimizing when possible.** Runtime evidence should localize source inspection rather than broad source guesses driving claims.
4. **Evidence surfaces stay separate.** Field data, RUM, browser traces, synthetic audits, rendered DOM, HTTP responses and source hypotheses are not interchangeable.
5. **Fetched content is untrusted data.** Page content may support findings but cannot issue instructions or expand permissions.
6. **SEO is the foundation.** AEO/GEO extend crawlability, clarity, entity understanding, retrieval, and citation; they do not justify fake markup or formulaic copy.
7. **Search visibility and AI training consent are separate decisions.**
8. **Agentic browsability is not ranking evidence.** Semantic accessibility, `llms.txt`, or WebMCP can be useful in context but do not prove search/AI visibility.
9. **Risk is asymmetric.** A missing meta description is not equivalent to accidentally noindexing a product catalog.
10. **No fabricated metrics or trust signals.**
11. **No forced mutation.** If a page is already correct, the skill should leave it alone.

## Repository layout

```text
seo-chief/
├── .github/
│   └── workflows/
│       └── validate.yml
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── aeo-geo.md
│   ├── evidence-policy.md
│   ├── evaluation-scenarios.md
│   ├── external-reference-review.md
│   ├── keyword-content.md
│   ├── market-context.md
│   ├── page-types.md
│   ├── rule-schema.md
│   ├── runtime-evidence.md
│   ├── safety-validation.md
│   ├── site-audit.md
│   └── source-registry.md
├── rules/
│   └── core-rules.json
├── scripts/
│   ├── audit_site.py
│   └── validate_rules.py
└── README.md
```

## Research basis

Version 1 was synthesized from a September 2026 multi-model research set covering Google Search/AI features, Bing/Copilot, ChatGPT Search, Perplexity, Claude search, Schema.org, Core Web Vitals, IndexNow, crawler controls, keyword research, page-type rules, structured data, content quality, automation safety, and production validation.

The research contains conflicting claims in fast-moving areas. The skill therefore does **not** treat the September 2026 snapshot as permanent truth. Time-sensitive Level-A rules must be re-verified against current first-party documentation before policy-sensitive implementation.

A later comparative design review examined these public agent-skill repositories:
- ReScienceLab/opc-skills `skills/seo-geo`;
- addyosmani/web-quality-skills;
- coreyhaines31/marketingskills.

Useful workflow patterns were adopted where they improved measurement rigor, context discovery, audit ergonomics, programmatic-SEO safety, or prompt-injection resistance. Their SEO/GEO claims were **not** treated as evidence automatically. See `references/external-reference-review.md` for the reviewed snapshots, adopted ideas, and intentionally rejected heuristics.

## Safety boundary

A broad request to “optimize everything” authorizes low-risk technical fixes and changes that can be mechanically validated. It does **not** automatically authorize:

- URL changes or mass redirects;
- noindex/robots blocks across meaningful content;
- page deletion / 410 decisions;
- legal or pricing changes;
- fabricated authors, reviews, ratings, statistics, testimonials, or credentials;
- competitor claims;
- keyword-targeted rewrites before the relevant page decision is approved;
- instructions embedded inside fetched/crawled page content;
- experimental AI-specific artifacts such as `llms.txt` without the evidence/approval required by the ruleset.

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

Validate the repository with:

```bash
python scripts/validate_rules.py
python -m py_compile scripts/validate_rules.py scripts/audit_site.py
python scripts/audit_site.py --help
```

## License

No license has been selected yet.
