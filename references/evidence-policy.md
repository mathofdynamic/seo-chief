# Evidence Policy

Use this reference whenever a recommendation depends on search-engine, AI-search, crawler, structured-data, performance, or measurement behavior.

## Evidence classes

| Class | Meaning | Skill behavior |
|---|---|---|
| `A` | Current first-party platform documentation, protocol specification, or standards body | May become an enforceable rule when applicable |
| `B` | Strong technical practice supported by reproducible evidence or broad expert consensus | Recommendation; validate where possible |
| `C` | Experimental, emerging, platform-specific, or weakly replicated | Optional experiment; never silently auto-apply |
| `D` | Unsupported, obsolete, contradicted, or folklore | Exclude or explicitly warn against |

Evidence class does not equal severity. A Level-A rule can be low impact; a Level-B production failure can be critical.

## Source priority

Prefer:
1. platform owner documentation;
2. standards/RFCs and Schema.org vocabulary;
3. first-party engineering/product documentation;
4. first-party webmaster tooling;
5. reproducible empirical research;
6. reputable technical SEO research;
7. expert commentary.

Do not cite generic SEO blogs when a first-party source exists.

## Freshness

Search and AI platform behavior changes quickly.

Before policy-sensitive implementation, re-verify current official guidance for:
- crawler names, purposes, robots behavior, and IP verification;
- Google generative Search guidance;
- Bing/Copilot search and AI reporting;
- structured-data rich-result support/deprecations;
- IndexNow participation/requirements;
- Core Web Vitals definitions;
- AI-specific files such as `llms.txt`;
- webmaster reporting features.

Record `last_verified` in machine-readable rules. If a rule is materially time-sensitive and stale, verify it before acting.

## Conflicting claims

When sources disagree:
1. identify the exact claim using `platform x surface x mechanism x intervention x outcome`;
2. prefer current first-party documentation for declared behavior;
3. keep empirical observations separate from official statements;
4. do not generalize one platform to another;
5. downgrade the confidence of unresolved claims;
6. do not auto-fix based on an unresolved C-level claim.

Example: “AI bots ignore robots.txt” is too broad. Evaluate each named agent separately.

## Numeric SEO data

Never fabricate:
- volume;
- CPC;
- difficulty;
- impressions;
- clicks;
- CTR;
- position;
- traffic;
- conversions;
- citation counts;
- competitor traffic;
- trend values.

For each numeric metric record:
- source;
- country/market;
- language;
- device when relevant;
- observation/export date;
- status: `measured`, `observed`, `estimated`, `modelled`, or `unavailable`.

Keep conflicting provider values separate. Do not average them silently. Google Trends is relative interest, not search volume.

## Causal claims

Do not say a change “will rank” or “will get cited.” Prefer:
- “required for eligibility” when officially required;
- “supports discoverability/clarity” when evidence is indirect;
- “experimental” when causal evidence is weak.

## Myth filter

Reject these as universal rules unless current evidence establishes otherwise:
- fixed keyword density;
- fixed minimum article length;
- “exactly 60 characters” for titles;
- universal one-H1 requirement;
- mandatory FAQ schema;
- schema as a direct ranking boost;
- `llms.txt` as a universal AI-ranking requirement;
- fixed 40–60 word answer blocks;
- repeated brand mentions as a citation hack;
- domain authority as a Google metric;
- robots.txt as a de-indexing mechanism.
