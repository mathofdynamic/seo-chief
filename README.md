# seo-chief

`seo-chief` is a repository-aware Codex skill for one-call SEO, AEO, and GEO operations across source code and production infrastructure.

It inspects first, plans internally, applies safe fixes, tests the result, deploys only when authorized and technically possible, validates production behavior, and reports evidence without requiring page-by-page conversation.

## What it covers

- crawlability, indexability, rendering, metadata, canonicals, redirects, robots, and sitemaps;
- page inventories, page types, internal links, structured data, media SEO, multilingual SEO, and Core Web Vitals diagnostics;
- AEO/GEO answer extraction, crawler policy, entity clarity, citation readiness, and brand discoverability;
- VPS + Nginx + PM2, Cloudflare Pages/Workers, Vercel, Netlify, static hosting, Docker/reverse proxy, GitHub Pages, and browser-only control panels;
- rollback-safe releases, artifact hashes, production response matrices, Markdown negotiation, `Accept`/`Vary` behavior, private-route protection, assets, and API health;
- machine-readable change manifests and one consolidated decision table for unresolved human decisions.

## Install

From the public repository:

```bash
npx skills add mathofdynamic/seo-chief --skill seo-chief --agent codex --copy --yes
```

For local validation or development:

```bash
python scripts/validate_skill.py
python scripts/validate_rules.py
python -m unittest discover -s tests -p "test_*.py"
```

## Invocation

```text
$seo-chief <repository and/or production URL>
```

Broad `fix`, `optimize`, `implement`, and `ship` requests use `autopilot` by default. Available modes and safety gates:

- `autopilot`
- `audit-only`
- `plan-only`
- `no-deploy`
- `no-merge`
- `no-push`

Example:

```text
Use $seo-chief https://example.com and D:\Projects\example.
Autonomously audit and optimize safe SEO/AEO/GEO issues, test the result, deploy only if the project deployment is authorized, validate production, and report unresolved decisions in one table.
```

## Repository layout

```text
seo-chief/
|-- SKILL.md
|-- agents/openai.yaml
|-- references/
|   |-- agent-readiness.md
|   |-- deployment-adapters.md
|   |-- execution-protocol.md
|   |-- response-validation.md
|   |-- ...
|-- rules/core-rules.json
|-- rules/operational-rules.json
|-- scripts/
|   |-- validate_response_matrix.py
|   |-- validate_rules.py
|   `-- validate_skill.py
|-- templates/
|   |-- change-manifest.json
|   |-- consolidated-decision-table.md
|   `-- production-response-matrix.json
`-- tests/
    |-- evaluation-scenarios.json
    |-- test_response_matrix.py
    `-- test_skill_contract.py
```

## Operating boundary

The skill can automatically apply deterministic, reversible, validated fixes. It does not invent business facts, reviews, ratings, addresses, prices, authors, competitor claims, search metrics, or external authority. It does not guarantee rankings, traffic, citations, or AI visibility. It does not push Git by default, modify neighboring services, or make destructive URL/indexability changes without the required approval.

Deployment and Git publication are separate actions. VPS releases use a scoped temporary release, local/remote hashes, Nginx syntax validation, health gates, and rollback evidence. Unknown HTML/Markdown routes, content negotiation, `Vary`, direct `.md` siblings, redirects, private routes, assets, API health, robots, sitemaps, and JSON-LD are validated through the response matrix helper.

## Rule database

`rules/core-rules.json` contains machine-readable rules with an executable contract:

```text
check -> expected -> fix -> validation
```

Run `python scripts/validate_rules.py` to validate rule IDs, enums, dates, evidence levels, source traceability, and automation gates.

## License

No license has been selected yet.
