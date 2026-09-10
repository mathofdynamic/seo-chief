# One-Call Execution Protocol

This reference defines the state machine for a broad `seo-chief` run. It is the operational contract behind the `autopilot` mode in `SKILL.md`.

## Input and mode resolution

Accept a repository path, production URL, or both. Resolve missing values from the checkout, deployment configuration, canonical metadata, sitemap, and authenticated provider context before asking the user.

Modes:

| Mode | Inspect | Mutate source | Build/test | Deploy | Git push/merge |
|---|---:|---:|---:|---:|---:|
| `autopilot` | yes | safe and validated changes | yes | only when authorized and technically possible | no by default |
| `audit-only` | yes | no | read-only checks only | no | no |
| `plan-only` | yes | no | no mutation | no | no |
| `no-deploy` | yes | safe and validated changes | yes | no | no by default |
| `no-merge` | yes | allowed by the selected mode | yes | allowed if separately authorized | no merge |
| `no-push` | yes | allowed by the selected mode | yes | allowed if separately authorized | no push |

`autopilot` is the default for broad requests containing verbs such as `fix`, `optimize`, `implement`, or `ship`, unless the user selects another mode. `no-deploy`, `no-merge`, and `no-push` are orthogonal safety gates and may be combined with `autopilot`.

An explicit mode always wins over inference. A deployment request is separate from a source-code fix request: deploy only when the user requested release/deployment or the active project instructions explicitly authorize it. Never infer Git publication from deployment authority.

## Run boundary and state

Create a run identifier and a temporary run directory outside the target repository. Keep transient crawls, response bodies, hashes, release archives, and manifests there unless the user explicitly requests a committed report. Do not add generated state to the target repository by default.

Maintain a machine-readable change manifest using `templates/change-manifest.json`. Every material change has one record with:

```text
check -> expected -> change -> local verification -> production verification -> rollback note
```

The manifest must record mode, repository root, production URL, active branch, detected deployment model, changed files, affected routes, evidence, automation class, test results, release/config identifiers, and whether Git was committed or pushed. Redact secrets and never record private keys, tokens, cookies, or authorization headers.

## Repository and worktree safety

1. Resolve the active repository with `git rev-parse --show-toplevel` and inspect the path requested by the user.
2. Enumerate nested `.git` directories and worktrees before reading or writing application files. A nested checkout is a separate repository boundary.
3. Inspect `git status --short --branch`, upstream, current branch, and recent history for every repository that may be touched.
4. Preserve unrelated dirty changes. Do not reset, clean, stash, checkout, rebase, or overwrite them without explicit authorization.
5. Restrict edits to the resolved project and files required by the finding. If a dirty change overlaps a required edit, preserve it, avoid destructive mutation, and record the conflict as a blocker while continuing read-only analysis elsewhere.
6. Never modify neighboring repositories, sibling services, shared reverse-proxy configuration, or unrelated deployment roots.

## Deterministic pipeline

Execute these steps in order. A step may be skipped only when it is genuinely not applicable; record the reason in the manifest.

1. **Resolve scope.** Identify repository, nested repositories, production URL, deployment target, active branch, selected mode, and authorization gates.
2. **Inspect worktrees.** Preserve dirty changes and establish the exact source/deployment boundary.
3. **Inventory routes.** Merge routes from source, router, sitemap, internal links, redirects, canonicals, CMS/data sources, and production.
4. **Crawl representative endpoints.** Fetch homepage, major templates, robots, sitemap, redirects, private-route samples, assets, API health, and agent-readiness variants.
5. **Build the Page Inventory.** Record normalized/final URLs, page type, status, indexability, canonical, locale, rendering, metadata, schema, links, entity, intent, findings, severity, automation, and validation state.
6. **Build the finding matrix.** Attach evidence and an automation class to every finding; distinguish repository truth from production truth.
7. **Implement safe fixes.** Apply all `safe-auto` and `auto-with-validation` changes inside the authorized scope. Do not stop at a plan.
8. **Add or update tests.** For every changed behavior, add project-native tests or a reusable endpoint assertion and update the manifest.
9. **Run project checks.** Run applicable build, lint, typecheck, unit/integration, route, render, schema, sitemap, robots, link, and performance checks.
10. **Validate artifacts.** Inspect the exact generated output, asset existence, HTML, headers, JSON-LD, redirects, and machine-readable files that will be released.
11. **Detect deployment model.** Use `references/deployment-adapters.md`; do not assume Git integration, hosting provider, web root, process name, or project ID.
12. **Create a scoped release.** Build an isolated release artifact or provider deployment and record hashes, release ID, previous release/config, and rollback action.
13. **Preflight activation.** Validate provider/project identity, environment, config syntax, target paths, secrets/bindings, health checks, and scope before activation.
14. **Deploy only the requested project.** Respect `no-deploy`, `no-merge`, and `no-push`. Keep production deployment separate from Git publication.
15. **Verify production.** Test exact live URLs, status codes, redirects, headers, HTML/Markdown variants, robots, sitemap, JSON-LD, assets, API health, canonical host, and private-route protections.
16. **Rescan.** If a supported CLI, API, Search Console/Bing mechanism, or public rescan endpoint exists and credentials/scope are available, run one bounded post-release rescan. Otherwise report that no external rescan was available or authorized.
17. **Report verified outcomes.** Return only observed changes, tests, deployment/config state, production evidence, remaining decisions, rollback location/command, and risks.

## Autopilot continuation rules

- Do not ask page-by-page questions. Group unresolved keyword, URL, redirect, legal, business, competitor, and external-authority decisions into one consolidated table.
- A broad approved request authorizes low-risk deterministic fixes and validated implementation fixes. Do not ask for the same broad approval again.
- If human information is missing, skip only the unsafe mutation, continue all independent work, and add one decision-table row with the exact missing input.
- `requires-inference` may be used only when the inference is high confidence, reversible, and validated. Otherwise batch it for review.
- `requires-human-info`, `requires-human-approval`, and `never` findings never become silent mutations.
- A deployment or rescan failure does not erase successful local work. Record the failed gate, preserve the rollback point, and continue report generation.

## Consolidated decision table

Use one table at the end of the run. Include only decisions that genuinely need human judgment, credentials, legal/business facts, or external authority.

| ID | Finding | URLs/scope | Evidence | Proposed action | Automation class | Required human input | Status |
|---|---|---|---|---|---|---|---|
| `D-001` | Example only | `/example` | Source/live evidence | Approve, revise, or skip | `requires-human-approval` | Exact decision or credential | `pending` |

Do not turn every passed check into a decision row. Use `status` values such as `pending`, `approved`, `skipped`, `blocked`, and `implemented`.
