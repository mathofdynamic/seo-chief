# Automation Safety and Validation

## 1. Automation classes

### `safe-auto`
Low-risk, deterministic, reversible changes that do not alter business claims, page intent, or meaningful URL/indexability strategy.

Examples:
- fix malformed metadata syntax;
- repair sitemap generation to exclude known noindex/error URLs;
- add missing image dimensions;
- correct obvious broken internal links when the intended target is unambiguous;
- fix schema syntax when visible facts already provide the values.

### `auto-with-validation`
Reasonable to implement automatically when authorized, but must be mechanically tested.

Examples:
- project-native canonical component fixes;
- JSON-LD generated from existing visible data;
- robots/sitemap generator corrections;
- rendering fixes;
- performance fixes;
- internal link additions with unambiguous context;
- IndexNow integration when applicable and non-destructive.

### `requires-inference`
The agent may propose or implement only with high confidence and validation.

Examples:
- page-type classification;
- intent inference;
- entity extraction;
- thin/commodity-content diagnosis;
- suggested internal-link relationships.

### `requires-human-info`
Cannot be truthfully completed from available evidence.

Examples:
- pricing terms;
- customer outcomes;
- author credentials;
- company history;
- legal status;
- competitor claims;
- business address/hours;
- private conversion data.

Never invent missing facts.

### `requires-human-approval`
High-impact, strategically meaningful, or potentially destructive.

Examples:
- URL/slug changes;
- redirects at scale;
- 404/410 decisions for existing content;
- noindex of meaningful currently public pages;
- broad robots Disallow;
- canonical consolidation across substantial sections;
- major keyword-targeted rewrites;
- page merge/delete;
- migration changes;
- training-crawler opt-in/opt-out policy when not already specified.

### `never`
Forbidden.

- fake reviews/ratings/testimonials;
- fake authors/credentials;
- invented prices or product claims;
- cloaking;
- hidden keyword text/links;
- doorway pages;
- link schemes;
- spun/scraped low-value pages;
- fake freshness/backdating;
- schema that contradicts visible content;
- mass thin AI content;
- manipulating legal text without explicit scope/review;
- bypassing authentication/access controls.

## 2. Severity

- `blocker`: prevents meaningful crawling/indexing/access for a major intended surface.
- `critical`: likely removes or severely distorts high-value visibility.
- `high`: material issue affecting a significant page/template set.
- `medium`: meaningful but limited impact.
- `low`: cleanup/quality improvement.
- `optional`: experiment or nonessential enhancement.

Do not inflate cosmetic metadata preferences into critical findings.

## 3. Approval semantics

A broad request such as “fully optimize the site” authorizes `safe-auto` and `auto-with-validation` work inside the requested domain/repository.

It does not authorize:
- destructive URL/indexability changes;
- business/legal fact invention;
- training-consent decisions;
- keyword-targeted content mutation before the page target is approved.

For site-wide content work, use one batch approval table instead of forcing serial approvals.

If the user explicitly authorizes a specific risky action, do not ask for the same approval again.

## 4. Validation layers

### Repository
Run applicable:
- build;
- lint;
- typecheck;
- unit/integration tests;
- framework route generation;
- static export generation.

### SEO mechanics
Check:
- robots syntax;
- sitemap XML;
- canonical output;
- metadata uniqueness;
- structured data parse/validation;
- hreflang reciprocity;
- status codes;
- redirects;
- broken links;
- image attributes;
- rendered initial HTML.

### Production
When live deployment is available:
- fetch representative URLs;
- verify real headers/status;
- verify redirects;
- inspect rendered HTML;
- inspect robots/sitemap;
- test crawler/WAF access;
- inspect mobile behavior;
- run field/lab performance evidence where available.

Never claim production verification when only source code was inspected.

## 5. Before/after evidence

For every material fix record:

```text
Finding:
Affected scope:
Severity:
Automation class:
Before:
Expected:
Change:
Validation:
After:
Evidence source:
Remaining risk:
```

## 6. Rollback discipline

For high-impact technical changes:
- identify affected URL set;
- preserve previous behavior/config;
- avoid mixing unrelated refactors;
- document rollback;
- validate on representative templates before broad rollout.

## 7. No-change outcome

Passing is a valid result.

If a page/template already meets the intended requirement:
- do not rewrite it for novelty;
- record the check as passed;
- identify only real remaining opportunities.

## 8. Execution-mode gates

`autopilot` is the default for broad fix/optimize requests. It must continue through safe implementation and validation instead of stopping after a plan. `audit-only` and `plan-only` prohibit source and deployment mutation. `no-deploy` prohibits activation even when source changes and tests are allowed. `no-merge` and `no-push` prohibit those Git actions independently of deployment.

Do not infer deployment, push, merge, or external rescan authorization from a general request to improve SEO. Keep each action in its own manifest field and report the actual state.

## 9. Deployment safety gates

Before a release, require:

- exact project/provider/server identity;
- scoped artifact and SHA-256 manifest;
- previous release/configuration reference;
- configuration preflight, including `nginx -t` for Nginx;
- process/API/public HTTP health checks;
- an executable project-scoped rollback action.

For a shared VPS, a successful file transfer is not deployment acceptance. Do not touch neighboring roots, processes, ports, Nginx sites, or services. Roll back automatically on activation or health failure when the previous scoped release is available.

## 10. Response and manifest evidence

For agent-readiness changes, validate HTML and Markdown variants of the same unknown URL, real `Content-Type`, `Vary` tokens, q-values, cache separation, direct `.md` siblings, redirects, private-route behavior, assets, API health, robots, sitemap, and JSON-LD. Do not rely on an untested server default.

Every material change must have a machine-readable record using `templates/change-manifest.json` with:

```text
check -> expected -> change -> local verification -> production verification -> rollback note
```

Never store credentials, private keys, cookies, authorization headers, or private response bodies in the manifest or test artifacts.
