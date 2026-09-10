# Source Registry

This is a verification index, not a frozen copy of platform rules. Re-check first-party sources before policy-sensitive implementation.

Last research synthesis: **2026-09-08**.

## Google

- `google-search-updates` — Google Search documentation updates
  https://developers.google.com/search/updates
- `google-search-essentials` — Google Search Essentials
  https://developers.google.com/search/docs/essentials
- `google-spam-policies` — Google Search spam policies
  https://developers.google.com/search/docs/essentials/spam-policies
- `google-ai-features` — Google Search guidance for AI features / generative optimization
  Resolve from current Search Central documentation; verify current URL via Search updates before use.
- `google-robots-meta` — robots meta/X-Robots controls
  Resolve from current Search Central documentation.
- `google-structured-data` — structured data feature documentation
  https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data

## OpenAI

- `openai-crawlers` — Overview of OpenAI crawlers
  https://developers.openai.com/api/docs/bots
- `openai-search-publisher` — ChatGPT Search publisher/discovery guidance
  Resolve from current OpenAI help/developer documentation when needed.

## Anthropic

- `anthropic-crawlers` — ClaudeBot / Claude-SearchBot / Claude-User policy
  https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler

## Perplexity

- `perplexity-robots` — Perplexity robots.txt behavior
  https://www.perplexity.ai/help-center/en/articles/10354969-how-does-perplexity-follow-robots-txt
- `perplexity-crawlers` — crawler/IP documentation
  Resolve from current Perplexity publisher/help documentation.

## Bing / Microsoft

- `bing-webmaster-ai-performance` — AI Performance in Bing Webmaster Tools
  https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
- `bing-webmaster-guidelines` — Bing Webmaster Guidelines
  Resolve from current Bing Webmaster documentation.
- `indexnow` — IndexNow protocol
  https://www.indexnow.org/

## Standards

- `rfc9309` — Robots Exclusion Protocol
  https://www.rfc-editor.org/rfc/rfc9309
- `schemaorg` — Schema.org vocabulary
  https://schema.org/

## Performance

- `webdev-cwv` — Core Web Vitals
  https://web.dev/vitals/

## HTTP and deployment

- `rfc9110` — HTTP Semantics, including status codes, content negotiation, and Vary
  https://www.rfc-editor.org/rfc/rfc9110
- `nginx-command-line` — Nginx command-line switches and configuration testing
  https://nginx.org/en/docs/switches.html
- `cloudflare-pages-deploy` — Cloudflare Pages direct upload and Wrangler deployment
  https://developers.cloudflare.com/pages/get-started/direct-upload/
- `cloudflare-pages-configuration` — Cloudflare Pages Wrangler configuration
  https://developers.cloudflare.com/pages/functions/wrangler-configuration/
- `vercel-deployments` — Vercel deployment environments and production release methods
  https://vercel.com/docs/deployments/overview
- `netlify-deployments` — Netlify deployment overview
  https://docs.netlify.com/site-deploys/overview/
- `github-pages` — GitHub Pages publishing model
  https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages

## Source handling

If a URL moves:
- locate the current official page;
- update this registry;
- update affected rules' last_verified;
- do not keep stale behavior simply because a URL changed.
