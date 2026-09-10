# Rule Database Contract

Every JSON file under `rules/` is a machine-readable rule pack. `rules/core-rules.json` contains foundational SEO rules and `rules/operational-rules.json` contains execution, deployment, HTTP, agent-readiness, and reporting gates. The prose references remain authoritative for nuance.

## Required fields

```json
{
  "id": "unique-kebab-case",
  "category": "technical-seo",
  "scope": "site|page|template|page-type",
  "applies_when": "plain-language condition",
  "check": "precise test",
  "expected": "desired observable state",
  "fix": "allowed remediation",
  "validation": "how to verify",
  "severity": "blocker|critical|high|medium|low|optional",
  "automation": "safe-auto|auto-with-validation|requires-inference|requires-human-info|requires-human-approval|never",
  "seo": true,
  "aeo": false,
  "geo": true,
  "evidence_level": "A|B|C|D",
  "sources": ["source-registry-id"],
  "last_verified": "YYYY-MM-DD",
  "notes": "optional"
}
```

## Rule quality bar

A rule must be executable as:

`check -> expected -> fix -> validation`

Do not add vague rules such as “improve SEO.”

A rule should identify:
- the condition under which it applies;
- the observable defect;
- what a safe fix means;
- how success can be tested;
- whether implementation needs approval.

## Evidence and freshness

- Level A rules with platform-specific behavior should cite an entry in `source-registry.md`.
- Time-sensitive rules need a real `last_verified` date.
- If current official documentation contradicts a stored rule, current documentation wins and the ruleset should be updated.

## Severity vs automation

These are independent.

Example:
- accidental sitewide noindex: `blocker`, `requires-human-approval` for strategy changes but safe to repair when clearly accidental and the user's scope authorizes restoration;
- missing social description: `low`, `auto-with-validation`.

## Extending the database

Prefer focused rules. Add framework-specific notes only when behavior materially differs.

Operational rules use the same contract as SEO rules. They must describe an observable check, expected state, safe fix, and validation evidence. Keep deployment and safety rules separate from provider-specific implementation details, and use evidence level B when the rule is an engineering control rather than a platform requirement.

Validate every rule pack, not only the core pack:

```bash
python scripts/validate_rules.py
```

Possible future rule packs include Next.js, Nuxt, Astro, SvelteKit, WordPress, ecommerce, and local SEO variants. Add each as a JSON file under `rules/` only when its behavior materially differs.
