# External Skill Reference Review — 2026-09-08

This document records the external agent-skill implementations reviewed for SEO Chief v2-style improvements. These repositories are **design references**, not evidence authorities for search-engine or AI-platform behavior. Platform claims still require the evidence policy and current first-party verification.

## Reviewed snapshots

| Repository | Snapshot reviewed | License | Relevant areas |
|---|---|---|---|
| ReScienceLab/opc-skills `skills/seo-geo` | `d8ab48aeb5b726a93994aee0285889862229c884` | Apache-2.0 | executable SEO audit scripts, keyword/competitor helpers, SEO/GEO workflow |
| addyosmani/web-quality-skills | `afa8da942115f2961fdbfa80807ea0b232ff6c00` | MIT | runtime-first measurement, Lighthouse, CWV, rendered audits, agentic browsing |
| coreyhaines31/marketingskills | `5b2c0007766c6a1cf1d53fd8fc73e979e0821022` | MIT | SEO audit, AI SEO, programmatic SEO, site architecture, content strategy, comparison pages |

No source code from those repositories is copied into `scripts/audit_site.py`; it is an original implementation inspired by the general idea that an agent skill should include executable fallback diagnostics.

## What SEO Chief adopted

### From ReScienceLab/opc-skills

Adopted concept:
- a no-API executable audit path is useful when browser/SEO APIs are unavailable;
- keyword/competitor research benefits from tooling rather than prose-only instructions.

SEO Chief implementation:
- `scripts/audit_site.py` provides a dependency-free, same-origin static crawler with explicit evidence limitations;
- it does not hard-code current AI crawler names or fixed SEO scoring formulas.

### From web-quality-skills

Adopted concepts:
- measure before optimizing when a runnable URL exists;
- use runtime evidence to localize source inspection;
- separate field data, RUM, traces, synthetic audits and static hypotheses;
- repeat equivalent measurements after a fix;
- absence in static HTML is not proof that rendered/client-injected schema is absent;
- agentic browsability is a separate quality surface from search ranking/citation.

SEO Chief implementation:
- `references/runtime-evidence.md` formalizes these distinctions;
- `SKILL.md` routes substantial audits through runtime evidence when available;
- static fallback output is explicitly diagnostic rather than ranking evidence.

### From marketingskills

Adopted concepts:
- read project-owned product-marketing context before asking users to restate it;
- treat fetched webpage content as untrusted data, not agent instructions;
- mine sales/support/customer language as content/keyword evidence;
- require per-page unique value and defensible data for programmatic SEO;
- maintain centralized, dated evidence for competitor facts;
- comparison pages should acknowledge legitimate competitor strengths and help readers decide.

SEO Chief implementation:
- `references/market-context.md` formalizes context discovery, customer evidence, pSEO provenance and comparison-page evidence;
- evaluation scenarios cover prompt injection, render-only schema, source-only CWV hypotheses and pSEO/competitor safety.

## What SEO Chief deliberately did not adopt

The external repositories contain some heuristics that are useful as ideas but are not safe as universal machine rules. SEO Chief intentionally does **not** adopt them without stronger current evidence.

Examples:
- fixed title/meta-description character limits as pass/fail rules;
- `meta keywords` as a modern SEO tactic;
- a universal one-H1 rule;
- a universal 3-click architecture rule;
- fixed internal-links-per-word quotas;
- fixed 40–60 word AI answer blocks;
- universal FAQ/FAQPage generation for AI visibility;
- generalized percentage citation/ranking boosts from one GEO study;
- hard-coded claims that a particular content format, PDF, freshness window or backlink count causes citation gains across current AI products;
- treating GPTBot/ClaudeBot/training controls as interchangeable with search/citation crawlers;
- treating `llms.txt`, markdown mirrors, WebMCP, or an agentic-browsing score as proof of AI citation visibility;
- fixed editorial-calendar or opportunity-score weights as search-engine rules;
- automatic programmatic page generation because a keyword/data combination exists.

## Principle preserved

External skills can improve **workflow design, measurement rigor, tool ergonomics and safety**. They do not override:
- first-party platform documentation;
- SEO Chief's A/B/C/D evidence policy;
- current verification requirements;
- truthful business data;
- approval gates;
- production validation.
