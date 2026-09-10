# AEO and GEO

## 1. Model

AEO and GEO are extensions of strong SEO, content quality, and entity clarity.

Use this split:

- **SEO:** discovery, crawling, indexing, relevance, representation.
- **AEO:** make genuine answers easy to identify and extract.
- **GEO:** improve eligibility for retrieval, grounding, citation, and correct entity attribution in generative systems.

Do not invent a universal “GEO ranking algorithm.”

## 2. Platform-specific behavior

Before changing production crawler policy, verify current first-party documentation.

At minimum distinguish:
- Google Search / AI Overviews / AI Mode;
- Bing / Copilot and Bing Webmaster AI reporting;
- ChatGPT Search;
- Perplexity;
- Claude search/web retrieval.

Do not transfer a rule from one platform to another without evidence.

## 3. Crawler taxonomy

Classify each bot by purpose before writing robots rules.

### Search / citation
Automated agents used to discover/index/retrieve content for search or cited answers.

Examples historically include:
- Googlebot
- Bingbot
- OAI-SearchBot
- Claude-SearchBot
- PerplexityBot

Names and behavior are time-sensitive. Re-verify.

### Training
Agents used to collect data that may contribute to foundation-model training.

Examples historically include:
- GPTBot
- ClaudeBot
- Google-Extended or other provider-specific training controls
- CCBot

Training consent is a business/legal policy choice. The skill must not silently opt a site in or out.

### User-triggered fetch
Agents that fetch a page because a user requested it.

Examples historically include:
- ChatGPT-User
- Claude-User
- provider-specific live retrieval agents

Robots behavior differs by provider and can change. Verify before asserting.

## 4. Default decision rule

For a commercial site whose goal is maximum search/AI discoverability:

- keep legitimate search/citation crawling available unless the user explicitly wants an opt-out;
- treat training crawler access as a separate owner decision;
- do not block user-triggered retrieval unless there is a privacy, licensing, abuse, or infrastructure reason;
- verify network/WAF access with official IP ranges or verified-bot systems when available.

Never merge all “AI bots” into one blanket robots rule.

## 5. Google generative Search

Use current Google Search documentation.

Current research basis indicates:
- standard Search crawl/index eligibility remains foundational;
- no special AI schema/file is required merely for AI Overviews/AI Mode;
- spam policies also apply to generative Search;
- non-commodity, helpful content remains central.

Therefore do not:
- add fake AI meta tags;
- rewrite every page into artificial “LLM chunks”;
- add FAQ schema solely for AI visibility;
- treat `llms.txt` as a Google ranking lever without current first-party evidence.

## 6. Answer extraction

When the page genuinely answers questions, improve extractability through normal editorial clarity:
- descriptive headings;
- direct factual sentences;
- concise definitions;
- steps for procedural content;
- lists/tables when they are the clearest representation;
- explicit units, dates, versions, names, and qualifiers;
- nearby supporting evidence;
- clear distinction between fact and opinion.

Do not force question headings or arbitrary 40–60 word answer lengths.

## 7. Generative citation readiness

For content that should become a cited source:
- state the page's subject/entity clearly;
- use consistent entity names;
- provide unique or first-hand information;
- support material claims;
- expose relevant text in crawlable HTML;
- keep dates/versions accurate;
- cite original sources where useful;
- avoid vague marketing-only copy;
- make important facts easy to identify in context;
- keep canonical and indexability clean;
- earn legitimate external mentions rather than manufacturing them.

A citation-friendly page is not necessarily long. It is specific, trustworthy, and useful.

## 8. Entity clarity

For organizations/products/people:
- use consistent canonical names;
- connect Organization/Product/Person entities only when real;
- use `sameAs` only for genuine authoritative profiles;
- maintain About/Contact/team information where relevant;
- align visible text, schema, social profiles, logo, and product naming;
- avoid fake Knowledge Graph manipulation.

## 9. `llms.txt` and AI-specific files

Treat as **optional/experimental** unless current platform documentation gives it a concrete role.

If implemented:
- generate it from canonical, maintained content;
- do not expose private/internal URLs;
- do not imply it controls training unless a provider says so;
- validate links;
- avoid duplicate stale mirrors;
- classify as optional in reports.

## 10. Off-site authority

The repository cannot directly create genuine authority.

Recommend, but do not automate spam:
- editorial links;
- original research/data;
- product documentation;
- public tools;
- case studies;
- citations;
- relevant community references;
- accurate profiles/listings.

Never use link schemes, fake reviews, mass directories, paid links without proper attributes, or synthetic “brand mention” campaigns.

## 11. Measurement

Separate observed outcomes from optimization hypotheses.

Traditional:
- GSC/Bing impressions, clicks, CTR, position;
- index coverage;
- crawl health;
- organic sessions/conversions.

Generative:
- Bing AI Performance / other first-party citation reports where available;
- referral traffic from AI products;
- server-log crawler activity;
- citation/brand-mention tracking for a defined prompt set.

Do not treat third-party “AI visibility scores” as ground truth.

## 12. WAF and bot diagnostics

For each intended crawler:
1. verify robots policy;
2. request robots.txt and representative public pages;
3. inspect status/challenge behavior;
4. validate IP/verified-bot identity where possible;
5. confirm the crawler can retrieve useful HTML;
6. record observed date.

A 200 to a normal browser does not prove crawler accessibility.
