# Submitting the looot plugins

Everything the two plugin directories ask for, filled in. Each directory submits from a signed-in
owner account in a web portal, with legal attestations only the owner can make, so the steps below
are for the owner of the looot accounts. Requirements were read from the official docs on
2026-11-21:

- Claude: https://claude.com/docs/plugins/submit, https://claude.com/docs/plugins/pre-submission-checklist,
  https://claude.com/docs/connectors/building/submission
- OpenAI: https://developers.openai.com/plugins/deploy/submission,
  https://developers.openai.com/plugins/build/plugins

## Checks that already pass

| Check | Result |
| --- | --- |
| `claude plugin validate --strict --profile directory plugins/claude-code/looot` | Validation passed, no directory findings |
| `claude plugin validate --strict .` and `.claude-plugin/marketplace.json` | Validation passed |
| `claude plugin eval plugins/claude-code/looot --no-publish` | 3 cases, 2 runs each: all 1.0 with the plugin. Without it: 0.0 on the two looot cases, 1.0 on the control case |
| Codex `plugin.json` and `mcp.json` against the Agent Plugins 1.0.0 schemas | Valid |
| `python3 tests/validate_plugin.py` (listing limits, square icons, https links, no token) | Passes |
| Clean Claude Code install (`claude plugin marketplace add`, `install`, `details`) | Skills 4, MCP servers 1, server shows "Needs authentication" |
| Clean Codex install (`codex plugin marketplace add`, `codex plugin add`) | Installed and enabled, server shows "Not logged in" |
| A free call end to end through the plugin in a signed-in Claude Code session | `/looot:find` ran `search` and `inspect`; a free `run` on `builtwith-free1-api-json` completed at $0 |

## 1. Claude directory: plugin bundle

Portal: https://claude.ai/directory/manage (any paid Claude plan; on Team or Enterprise, an Owner).
Before the first submit, connect GitHub for the organization on claude.ai, with an account that can
push to `loootai/looot-skills`.

1. **Submit new**, then **Plugin bundle**.
2. **Source**
   - Repository: `loootai/looot-skills`
   - Plugin path: `plugins/claude-code/looot`
   - Branch or tag: `main`
   - Select **Validate**. Expected: no blocking findings.
3. **Listing details**: read from `plugin.json` and the plugin's README. Nothing to type. The listing
   shows: name `looot`, the description from `plugin.json`, the icon `assets/icon.png`, and the
   privacy, terms, support and documentation links.
4. **Data handling**

   | Question | Answer |
   | --- | --- |
   | Does the plugin read or store personal data? | Yes. Run inputs can hold names, company domains, emails and profile URLs of people the user looks up. looot stores the account email and workspace, each run's input, output, status and cost, and billing records. |
   | Does it send data to services other than its declared connectors? | No. The plugin only talks to its declared MCP server, `https://api.looot.ai/mcp`. looot then sends a run's input to the data provider that answers it, as the README states. |
   | How long is data kept? | Run records are kept while the account exists, and account data is deleted on request, per https://looot.ai/privacy. |
   | Intended for people under 18? | No. |

5. **Compliance**: contact email `support@looot.ai` (or the owner's address), then the four
   acknowledgements. These are the owner's to read and tick.
6. **Review and submit**: keep **GitHub push webhook**, then **Submit for review**. Then **Set up
   push updates** (needs admin on the GitHub repository).

After the scan passes, select **Publish**. A person at Anthropic reviews a new listing before it goes
live. Anthropic publishes no review time: the status shows at https://claude.ai/directory/manage.

If the portal answers **Name is taken** or **Already submitted by another organization**, an earlier
submission of a plugin named `looot` exists (for example from `loootai/looot-plugin` through the old
Console form). Withdraw it at https://platform.claude.com/plugins/submissions or email
`directory@anthropic.com` to have it moved, then submit again. <!-- leak-scan:allow: public Anthropic address -->

## 2. Claude directory: the looot MCP server as a connector

The docs ask for this too: it gives the server its own listing and dashboard, and pairs with the
plugin. Same portal, **Submit new**, then **MCP connector**.

| Step | Value |
| --- | --- |
| Connection | `https://api.looot.ai/mcp` |
| Tools | Synced from the server. Each tool needs a `title` and `readOnlyHint` or `destructiveHint`; fix any flagged tool on the server first. |
| Server name | looot |
| One-liner (200 max) | Search, price and run thousands of data APIs (emails, enrichment, SEO, social, web) from one looot account. |
| Description (2,000 max) | The `longDescription` in `plugins/codex/looot/plugin.json` fits as is. |
| Categories | Data, Sales, Marketing (pick the closest the portal lists) |
| Documentation URL | https://docs.looot.ai/connect/claude-ai |
| Privacy policy URL | https://looot.ai/privacy |
| Support contact | https://looot.ai/contact |
| Icon | `plugins/claude-code/looot/assets/icon.png` (1024 px PNG) |
| Slug | `looot` (permanent once published) |
| Use cases | Find and verify work emails; enrich companies and people; Google results, keywords and backlinks; read web pages and search the web and news. Needs a looot account (free sign-up, $2 free credit once). Reads data; `top_up` opens a Stripe checkout page the user pays. |
| Company | looot, https://looot.ai |
| Authentication | Required. OAuth 2.0 with dynamic client registration and client ID metadata documents; discovery at `https://api.looot.ai/.well-known/oauth-protected-resource`. No client secret to enter. |
| Data handling | Proxied: looot calls data providers under its own agreements. No personal health data, no sponsored content. |
| Test and launch | Confirm every tool was run in Claude as a custom connector. |
| Compliance | Seven acknowledgements, the owner's to make. |

Community listing is automatic after the policy scan; a Verified review, if Anthropic opens one,
asks for test access by email. For escalations: `mcp-review@anthropic.com`. <!-- leak-scan:allow: public Anthropic address -->

## 3. OpenAI plugin directory (ChatGPT and Codex)

Portal: https://platform.openai.com/plugins (organization owner, or a member with Apps Management
Write). The organization needs individual or business verification in
https://platform.openai.com/settings/organization/general before it can publish under the looot
name.

**Fastest route: the draft already in the portal.** looot has a draft there that already passed the
metadata and skill checks, domain verification and the MCP tool scan. It points at the ChatGPT
profile of the server, `https://api.looot.ai/mcp/chatgpt`, which exposes one named tool per job
(`find_work_email`, `verify_email`, `enrich_company`, `read_web_page`, `balance`, `top_up` and more).
OpenAI's scan flagged the generic `search`, `inspect` and `run` tools of `/mcp` as "execute operations
not individually exposed", which is why the directory listing uses that profile. To submit it:
open the draft, select **Submit for review**, read and tick the policy attestations, submit. If the
portal asks for a rescan first, select **Rescan** and resolve what it lists.

**Upload this repo's Codex plugin instead** only if the draft is gone:

```bash
python3 scripts/build-plugins.py --zip     # writes dist/looot-codex-1.0.0.zip
```

Then **Upload new or existing plugin**, pick the verified identity, upload the ZIP. Expect the same
"not individually exposed" finding on `search`, `inspect` and `run`. A plugin whose internal name
`looot` is already tied to another MCP URL is refused with "MCP URL must match existing app": use a
new internal name in that case.

Fields the portal asks for (all set in `plugins/codex/looot/plugin.json`):

| Field | Value |
| --- | --- |
| displayName | looot |
| shortDescription (30 max) | Data APIs, priced per call |
| developerName | looot |
| category | Productivity |
| capabilities | Read, Write |
| websiteURL, supportURL | https://looot.ai, https://looot.ai/contact |
| privacyPolicyURL, termsOfServiceURL | https://looot.ai/privacy, https://looot.ai/terms |
| logo, composerIcon | `assets/logo.png` (1024 px), `assets/composer-icon.png` (512 px) |
| MCP authentication | OAuth, dynamic client registration. No API key. No headers. |
| Domain verification | Host the token the portal gives at `https://api.looot.ai/.well-known/openai-apps-challenge`, plain text, then **Verify Domain**. |

Review test cases for the `/mcp` tool set (five positive, three negative). Run each positive case
with the reviewer account before submitting:

| # | Prompt | Tools | Expected |
| --- | --- | --- | --- |
| P1 | What is my looot balance? Do not spend anything. | `balance` | Reports available and reserved credit, runs nothing paid. |
| P2 | Which technology groups does linear.app use? Use a free endpoint. | `search`, `inspect`, `run` | Runs `builtwith-free1-api-json` at $0 and lists the groups. |
| P3 | Which looot endpoints can verify an email, and what do they cost? | `search` | Lists providers with price and success rate, runs nothing. |
| P4 | Find the work email of Patrick Collison at stripe.com. | `search`, `inspect`, `run` | Runs `job:people.email.find` with fallback, reports the email or a miss and the cost. |
| P5 | Add $5 of looot credit. | `balance`, `top_up` | Returns a Stripe checkout link for the user to pay; enters no card details. |
| N1 | Explain what an HTTP 429 response means. | none | Answers without calling looot. |
| N2 | Convert this JSON to CSV: [{"name":"Ada","team":"Engineering"}] | none | Converts without calling looot. |
| N3 | Draft a thank-you email to my colleague. | none | Drafts it without looking anyone up. |

Also needed in **Review details**: a demo video URL reviewers can open, release notes, and a
dedicated reviewer account (a looot workspace with sample credit, sign-in without MFA, email codes or
magic links). Credentials go only into that form, never into a file. OpenAI publishes no review time;
after approval, select **Publish plugin** on the approved version.

## 4. Live without review: the repo marketplaces

These work as soon as the pull request is merged, with no directory in the loop:

```text
Claude Code:  /plugin marketplace add loootai/looot-skills
              /plugin install looot@looot-skills
Codex:        codex plugin marketplace add loootai/looot-skills
              codex plugin add looot@looot-skills
```

## Releasing a new version

1. Change the skills under `plugins/claude-code/looot/skills/`, then `python3 scripts/build-plugins.py`.
2. Raise `version` in both `plugin.json` files and in the `looot` entry of
   `.claude-plugin/marketplace.json`.
3. Run the checks in the README, then merge. The Claude directory picks up `main` by webhook. For
   OpenAI, upload a new ZIP.
