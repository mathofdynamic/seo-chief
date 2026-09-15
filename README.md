# seo-chief

`seo-chief` is a repository-aware Codex skill for one-call SEO, AEO, GEO, and agent-readiness operations across source code and production infrastructure.

It inspects first, plans internally, applies safe fixes, tests the result, deploys only when authorized and technically possible, validates production behavior, runs an additive Is Agentic closure loop against public production, and reports evidence without requiring page-by-page conversation.

## What it covers

- crawlability, indexability, rendering, metadata, canonicals, redirects, robots, and sitemaps;
- page inventories, page types, internal links, structured data, media SEO, multilingual SEO, and Core Web Vitals diagnostics;
- AEO/GEO answer extraction, crawler policy, entity clarity, citation readiness, and brand discoverability;
- Is Agentic/Ora agent-readiness scoring, current report recommendations, Prompt to improve guidance, selective live check re-runs, fresh full rescans, and a `100/100`-or-blocker closure rule;
- VPS + Nginx + PM2, Cloudflare Pages/Workers, Vercel, Netlify, static hosting, Docker/reverse proxy, GitHub Pages, and browser-only control panels;
- rollback-safe releases, artifact hashes, production response matrices, Markdown negotiation, `Accept`/`Vary` behavior, private-route protection, assets, and API health;
- machine-readable change manifests and one consolidated decision table for unresolved human decisions.

The Is Agentic stage is additive. It does not replace or weaken the existing SEO/AEO/GEO workflow. Scanner recommendations are treated as external evidence, independently verified, and never used to justify fake APIs, MCP servers, auth flows, payment surfaces, business facts, or other score-gaming changes.

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
Autonomously audit and optimize safe SEO/AEO/GEO issues, test the result, deploy only if the project deployment is authorized, validate production, run the Is Agentic closure loop until a fresh 100/100 or a verified blocker, and report unresolved decisions in one table.
```

## Repository layout

```text
seo-chief/
|-- SKILL.md
|-- agents/openai.yaml
|-- references/
|   |-- agent-readiness.md
|   |-- is-agentic-closure-loop.md
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

The skill can automatically apply deterministic, reversible, validated fixes. It does not invent business facts, reviews, ratings, addresses, prices, authors, competitor claims, search metrics, external authority, or product surfaces merely to improve a scanner score. It does not guarantee rankings, traffic, citations, or AI visibility. It does not push Git by default, modify neighboring services, or make destructive URL/indexability changes without the required approval.

Deployment and Git publication are separate actions. VPS releases use a scoped temporary release, local/remote hashes, Nginx syntax validation, health gates, and rollback evidence. Unknown HTML/Markdown routes, content negotiation, `Vary`, direct `.md` siblings, redirects, private routes, assets, API health, robots, sitemaps, and JSON-LD are validated through the response matrix helper.

After the normal production verification, `references/is-agentic-closure-loop.md` reads the current Is Agentic/Ora findings, uses their concrete recommendations and generated Prompt to improve as advisory implementation input, verifies each issue, fixes applicable items, re-checks affected IDs live where possible, and runs a fresh full score. Completion is either `VERIFIED 100/100` or `BLOCKED at <score>/100` with the exact remaining check IDs and required external/human action.

## Rule database

`rules/core-rules.json` contains machine-readable rules with an executable contract:

```text
check -> expected -> fix -> validation
```

Run `python scripts/validate_rules.py` to validate rule IDs, enums, dates, evidence levels, source traceability, and automation gates.

## License

No license has been selected yet.
