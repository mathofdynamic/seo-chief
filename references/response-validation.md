# Reusable Response Validation

`scripts/validate_response_matrix.py` is a project-neutral helper for live or captured endpoint evidence. It uses only the Python standard library and is intentionally independent of a web framework, hosting provider, or test runner.

## Supported checks

The matrix can assert:

- raw HTML body and heading/content presence;
- title, meta description, canonical, `lang`, robots directives, and H1;
- JSON-LD syntax and `@type` values;
- robots.txt directives and sitemap XML validity;
- Markdown UTF-8 content and public recovery links;
- `Accept` representation negotiation and q-values;
- `Content-Type`, `X-Robots-Tag`, `Vary`, `Cache-Control`, and `Location` headers;
- 404/410 HTML and Markdown variants;
- redirect targets and host canonicalization;
- private-route noindex/auth behavior;
- asset existence and non-empty responses;
- API health response status and JSON shape;
- paired response/cache variant separation;
- a complete production response matrix.

## Usage

Fill in `templates/production-response-matrix.json`, then run:

```bash
python scripts/validate_response_matrix.py --spec path/to/production-response-matrix.json
```

The command captures responses without following redirects unless a case explicitly requests it, validates every expected assertion, and exits non-zero on any failure. It does not print response bodies or request credentials. For offline regression checks, provide a captured matrix:

```bash
python scripts/validate_response_matrix.py --captured path/to/captured-matrix.json
```

The captured format is the same as the generated output, so local fixtures and production evidence use one contract.

## Evidence boundary

A passing helper proves only the assertions in the supplied matrix at the observed time. It does not prove search indexing, ranking, citation, or business outcomes. Store the matrix and manifest outside the application checkout unless the user asks for a committed report.
