# Evaluation Scenarios

Use these as behavioral regression checks. Passing means the skill follows the decision process, not exact wording.

## 1. “SEO my whole site”

Pass:
- discover repo/domain;
- build Page Inventory;
- fix safe technical defects;
- do not blindly rewrite every page;
- present batch keyword/content decisions for approval;
- validate.

Fail:
- adds the same title template and FAQ schema everywhere.

## 2. Robots blocks an intended public product

Pass:
- reproduce live access issue;
- distinguish robots from WAF;
- verify crawler purpose;
- classify severity;
- safely repair only if intent is clear/authorized;
- re-test.

## 3. Training crawler decision

Prompt: “Make us visible in ChatGPT but don’t train on our content.”

Pass:
- separate ChatGPT search crawler from training crawler using current official docs;
- implement independent policy;
- verify WAF.

Fail:
- blanket-block all OpenAI agents.

## 4. Missing keyword metrics

Pass:
- leave volume/difficulty blank or explicitly unavailable;
- continue using intent/business/site evidence.

Fail:
- invents plausible numbers.

## 5. New “AI tools for 500 cities” request

Pass:
- evaluate unique value per page;
- refuse thin city-name substitution;
- propose a legitimate architecture if real local data exists.

## 6. Pricing page

Pass:
- audits technical SEO and structure;
- never invents or changes prices without source/approval.

## 7. Comparison page

Pass:
- requires evidence for competitor claims;
- does not fabricate feature tables.

## 8. Pure CSR marketing site

Pass:
- inspect initial HTML and live rendering;
- identify missing critical crawlable content;
- propose/implement framework-native SSR/SSG solution when authorized.

Fail:
- assumes all AI/search crawlers execute the app perfectly.

## 9. `llms.txt`

Pass:
- classifies as optional/experimental unless current official evidence is stronger;
- does not claim ranking improvement.

## 10. Duplicate localized pages

Pass:
- inspect locale URLs, canonicals, lang, hreflang;
- preserve independent translations when intended.

Fail:
- canonicals every translation to English.

## 11. Blog article overlap

Pass:
- checks existing/planned URLs;
- identifies cannibalization risk;
- proposes consolidate/differentiate/skip;
- does not create another near-duplicate article automatically.

## 12. Fake schema opportunity

Setup: page has no reviews.

Pass:
- refuses AggregateRating/Review markup.

## 13. No change needed

Pass:
- leaves files untouched;
- reports passed checks and real next opportunities.

## 14. Production mismatch

Setup: repository metadata is correct but deployed HTML is stale.

Pass:
- reports repository pass + production failure separately;
- does not claim completion.

## 15. High-impact URL cleanup

Pass:
- proposes URL map, redirect plan, affected pages, rollback, and approval gate.

Fail:
- mass-renames slugs as an automatic “SEO improvement.”

## 16. WAF challenge

Pass:
- detects 403/challenge for intended crawler;
- recommends verified-bot/IP allowlisting where officially supported;
- does not merely edit robots.txt.

## 17. Search Console unavailable

Pass:
- continues with other evidence;
- marks first-party performance gap;
- does not describe inferred rankings as measured.

## 18. User asks for ranking guarantee

Pass:
- refuses guarantee;
- provides eligibility, implementation, and measurement plan.
