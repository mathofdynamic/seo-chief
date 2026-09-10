# Agent-Readiness and Production Response Checks

These checks are endpoint behavior tests, not claims that a site will rank or be cited. Run them against the exact production host after deployment when deployment is in scope, and record the observed date, URL, request headers, status, response headers, and body assertions in the response matrix.

## Required response matrix

Use `templates/production-response-matrix.json` and `scripts/validate_response_matrix.py`. At minimum test:

| Case | Request | Expected |
|---|---|---|
| Normal HTML | unknown or known URL, no special `Accept` | normal HTML representation and truthful status |
| Unknown HTML | unique missing path, `Accept: text/html` | `404` or `410`, useful HTML recovery body, noindex protection where appropriate |
| Unknown Markdown | same missing path, `Accept: text/markdown` | same `404`/`410`, real `text/markdown` body, not a `200` SPA shell |
| Markdown q-value | same missing path, `Accept: text/markdown;q=0.9, text/html;q=0.8` | Markdown variant with the same error status |
| Direct Markdown sibling | existing and unknown `.md` paths | existing file follows documented behavior; unknown file remains a truthful error |
| Cache variant | same URL with HTML and Markdown requests | `Vary` separates `Accept`; include `Accept-Encoding` when compression varies |
| Redirect | HTTP/HTTPS, apex/www, trailing slash, known moved URL | one intentional redirect to the canonical host/path, no loop or unrelated homepage target |
| Private route | login/account/admin sample | authentication or denial plus `noindex` where the response is public enough to be crawled; no private data |
| Machine-readable | `/robots.txt`, sitemap URL(s), JSON-LD pages, optional `llms.txt` | parseable and internally consistent |
| Asset/API | favicon, OG image, service worker if present, health endpoint | expected status, content type, and non-empty/valid body |

## 404 and Markdown negotiation

For an unknown path:

1. Without a special header, verify HTML/default behavior and `404`/`410` status.
2. With `Accept: text/html`, verify `Content-Type: text/html` and a useful navigation/recovery body.
3. With `Accept: text/markdown`, verify the same `404`/`410` status, `Content-Type: text/markdown` with a UTF-8 charset when possible, and a genuine Markdown body.
4. Repeat with q-values, including `text/markdown;q=0.9`.
5. The Markdown body must expose at least one valid recovery link to `sitemap.xml`, `llms.txt`, documentation, or another public entry point. Do not link to private routes.
6. Verify `X-Robots-Tag: noindex, nofollow` or an equivalent safe error-page policy where the server exposes the error response to crawlers.
7. Verify that an unknown route does not return a `200` SPA shell for either representation.

The HTML and Markdown variants may share a route handler, but they must not share an incorrect status, cached representation, or content type. A direct `.md` sibling is a separate test; do not assume content negotiation makes it valid.

## Headers and cache separation

Header names are case-insensitive. Parse `Vary` as a comma-separated token set and require `Accept` whenever the representation changes by `Accept`. Include `Accept-Encoding` whenever compression changes by that request header. Test both absent and explicit `Accept` headers, q-values, and repeated requests with cache-busting query values or a fresh cache context.

Do not rely on an untested Nginx `default_type` variable or a framework default. Inspect the real `Content-Type`, `Vary`, `Cache-Control`, `ETag`, and redirect headers returned by the deployed server.

## HTML, Markdown, and machine-readable checks

For representative public HTML, validate:

- status and final canonical host;
- title, description, H1, and canonical link;
- `lang`, robots meta, and `X-Robots-Tag`;
- raw HTML visibility of primary content and crawlable links;
- JSON-LD parsing and visible-fact parity;
- asset URLs and Open Graph image existence.

For robots and sitemap files, validate syntax, URL status, canonical alignment, and absence of private/noindex/error URLs. For JSON-LD, parse every script block and reject malformed or unsupported fabricated facts. For Markdown, validate UTF-8 decoding, headings/links, no credentials, and public recovery links.

## Brand discoverability

When a production URL and an external search source are available, perform at least one current search for the canonical brand/product name and record the source and date. Do not present a search result as a ranking guarantee.

Classify the result into one or more of:

1. **Missing on-site entity signals:** automatically improve truthful, source-backed on-site signals when the canonical identity is clear: consistent brand name, title, visible header/footer, Open Graph site name, application name, Organization/WebSite/SoftwareApplication schema, About/contact/trust links, and canonical apex domain.
2. **Indexing delay:** on-site signals are present but the external source has not refreshed. Report observation and wait; do not fabricate authority.
3. **Generic or conflicting brand name:** flag the ambiguity and propose a human-approved naming/positioning decision before changing substantive copy.
4. **Missing external authority:** keep the on-site improvements, then put Search Console, Bing Webmaster, NAP, verified listings, press, legitimate editorial links, and other external-authority work in the consolidated decision table. Credentials or human relationships are required.

Never create fake brand mentions, fake profiles, synthetic reviews, link schemes, or guarantees that on-site entity signals will produce rankings, traffic, citations, or AI visibility.

## External rescans

After a verified deployment, use a supported CLI/API/public rescan mechanism when available and authorized. Bound the rescan to the affected route set or documented sample, record the tool/source/date, and separate “rescan requested” from “indexing/citation outcome observed.” If no such mechanism is available, report the limitation rather than claiming an external re-crawl.
