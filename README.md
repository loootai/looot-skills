<p align="center"><img src="assets/hero.png" alt="looot-skills: agent skills for looot, 10 free and 20 paid data jobs" width="100%"></p>

# looot skills

[![License](https://img.shields.io/github/license/loootai/looot-skills)](LICENSE) [![Release](https://img.shields.io/github/v/release/loootai/looot-skills)](https://github.com/loootai/looot-skills/releases) [![Docs](https://img.shields.io/badge/docs-docs.looot.ai-12A06A)](https://docs.looot.ai/?utm_source=github&utm_medium=readme&utm_campaign=looot-skills)

Agent skills for [looot](https://looot.ai/?utm_source=github&utm_medium=readme&utm_campaign=looot-skills): one key and one prepaid balance for 4,392 data API endpoints from 324 providers. Each folder under `skills/` is one skill in the [Agent Skills](https://agentskills.io) format (`SKILL.md` with `name` and `description` frontmatter). The agent searches the catalog, sees the price before it runs, and pays per call. A failed call costs nothing.

There are 31 skills. Ten of them run free. Twenty are paid data jobs. `looot` is the base skill.

## The looot plugin for Claude Code and Codex

Want the looot MCP server with browser sign-in and the core flow (search, inspect, run, balance, top up) in one install? Use the `looot` plugin in [`plugins/`](plugins):

| Client | Install | Sign in |
| --- | --- | --- |
| Claude Code | `/plugin marketplace add loootai/looot-skills` then `/plugin install looot@looot-skills` | `/mcp`, pick looot, Authenticate |
| Codex | `codex plugin marketplace add loootai/looot-skills` then `codex plugin add looot@looot-skills` | `codex mcp login looot` |

It adds three commands in Claude Code: `/looot:setup` (sign-in and a first free search), `/looot:find <job>` (compare providers and prices, runs nothing) and `/looot:balance [amount]` (credit and a Stripe top-up link). Details: [Claude Code plugin](plugins/claude-code/looot/README.md), [Codex plugin](plugins/codex/looot/README.md). The Codex skills are generated from the Claude Code ones by `python3 scripts/build-plugins.py`.

## Ten skills that run free

These call $0 endpoints, so the run costs nothing and needs no top-up. looot has no trial credit and a new workspace starts at $0. looot refuses a run only when its price is above your balance, so a $0 endpoint runs on a new account. You still sign in once (`looot login`). Each skill below was run for real on 2026-11-15, and its "Example output" section is trimmed from that run.

| Skill | What it returns | Source |
| --- | --- | --- |
| `looot-website-tech-stack` | Technology groups a domain uses (JavaScript, analytics, payment, CDN, hosting), with live and dead counts | BuiltWith free API |
| `looot-cve-exploited-check` | Whether a CVE is on the CISA known exploited list, the date added, the action due date, CVSS scores | NIST NVD |
| `looot-clinical-trials-search` | Studies by condition, drug, sponsor or place: NCT id, phase, status, sponsor, sites | ClinicalTrials.gov |
| `looot-lei-company-lookup` | A company's LEI, exact legal name, addresses, entity and registration status | GLEIF |
| `looot-sec-filings` | A US public company's CIK, profile and recent filings (10-K, 10-Q, 8-K, Form 4) | SEC EDGAR |
| `looot-research-papers` | Papers by topic: title, authors, journal, year, citations, open access, DOI | OpenAlex |
| `looot-npm-package-check` | Latest version, license, dependencies, provenance, and every security advisory with its fix version | npm registry, OSV.dev |
| `looot-vehicle-recalls` | A decoded VIN and every US safety recall for that make, model and year | NHTSA |
| `looot-fda-drug-recalls` | Drug recalls by drug, firm or reason: class, status, dates, lots | openFDA |
| `looot-sanctions-check` | Matches for a name on the OFAC SDN, UK and EU sanctions lists, with score and official link | Official lists via looot |

Cost per run for all ten: $0 (free, no top-up needed). If `looot inspect` ever shows a price above $0, the skill tells the agent to say so and ask first.

## Paid data jobs

These run on paid provider endpoints. Searching and inspecting are free. A run needs credit at the price `looot inspect` shows, so the first paid run needs a $5 top-up (the minimum). They are the same files looot publishes at https://looot.ai/agent-skills?utm_source=github&utm_medium=readme&utm_campaign=looot-skills.

| Skill | What it does | Cost |
| --- | --- | --- |
| `looot-ai-search-visibility` | Check AI search visibility | needs a $5 top-up |
| `looot-amazon-product` | Look up an Amazon product | needs a $5 top-up |
| `looot-backlink-checker` | Check a domain's backlinks | needs a $5 top-up |
| `looot-company-email-format` | Find a company's email format | needs a $5 top-up |
| `looot-company-list-builder` | Build a company list | needs a $5 top-up |
| `looot-domain-keywords` | Find the keywords a domain ranks for | needs a $5 top-up |
| `looot-email-verification` | Verify an email address | needs a $5 top-up |
| `looot-enrich-a-company` | Enrich a company | needs a $5 top-up |
| `looot-enrich-a-person` | Enrich a person | needs a $5 top-up |
| `looot-find-phone-numbers` | Find a phone number | needs a $5 top-up |
| `looot-find-professional-emails` | Find a professional email | needs a $5 top-up |
| `looot-google-maps-reviews` | Read Google Maps reviews | needs a $5 top-up |
| `looot-google-serp` | Read a Google results page | needs a $5 top-up |
| `looot-job-postings` | Search job postings | needs a $5 top-up |
| `looot-keyword-volume` | Check keyword volume and CPC | needs a $5 top-up |
| `looot-local-business-search` | Find local businesses | needs a $5 top-up |
| `looot-meta-ads-library` | Read a company's Meta ads | needs a $5 top-up |
| `looot-reddit-search` | Search Reddit | needs a $5 top-up |
| `looot-tiktok-search` | Search TikTok | needs a $5 top-up |
| `looot-youtube-transcript` | Get a YouTube transcript | needs a $5 top-up |

Each free skill ends with a "Next step" that names one of these paid jobs, for example `looot-website-tech-stack` leads to `looot-company-list-builder`.

The base skill, `looot`, connects the MCP server, searches the catalog, reads prices and runs endpoints with fallback.

## Install

Pick one of three ways.

**With the skills CLI.** Installs into Claude Code, Cursor, Codex and the other agents the [skills CLI](https://github.com/vercel-labs/skills) supports. Add `--list` to see the skills first, or `--skill looot-sec-filings` to install one.

```bash
npx skills add loootai/looot-skills
```

**As a Claude Code plugin.** Installs all 31 skills and the looot MCP server in one go. The repo root is the plugin (`.claude-plugin/plugin.json`), so the plugin ships the same `skills/` folder.

```
/plugin marketplace add loootai/looot-skills
/plugin install looot-skills@looot-skills
```

**By copying a folder.** Each skill is one folder with one `SKILL.md`.

```bash
git clone https://github.com/loootai/looot-skills
cp -r looot-skills/skills/looot-sec-filings ~/.claude/skills/
```

Then set looot up once (the plugin already adds the MCP server):

```bash
npm install -g looot@1.4.0
looot login
claude mcp add --transport http looot https://api.looot.ai/mcp
```

The full guide is at https://looot.ai/skill.md?utm_source=github&utm_medium=readme&utm_campaign=looot-skills (the `looot` skill in this repo covers the same ground).

See also: [awesome-looot-use-cases](https://github.com/loootai/awesome-looot-use-cases) (copy-paste recipes), [awesome-gtm](https://github.com/loootai/awesome-gtm) (open-source GTM tools) and [looot-plugin](https://github.com/loootai/looot-plugin) (the base plugin for Claude Code, Codex and Cursor).

## Cost

The skill files are free. Searching and inspecting are free. The ten free skills run at $0. A paid run is billed per call at the price `looot inspect` shows first, and needs a top-up of $5 minimum, since looot has no trial credit.

## Checks

```bash
python3 tests/validate_plugin.py                                   # marketplaces, plugins and skill files
python3 scripts/build-plugins.py --check                           # Codex skills match the Claude Code ones
claude plugin validate --strict --profile directory plugins/claude-code/looot
claude plugin eval plugins/claude-code/looot --no-publish          # 3 cases on a mocked looot server
bash scripts/leak-scan.sh                                          # no keys, tokens or private hosts
```

## License

MIT. See [LICENSE](LICENSE).
