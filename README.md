<p align="center"><img src="assets/hero.png" alt="looot-skills: 20 data jobs as agent skills" width="100%"></p>

# looot skills

[![License](https://img.shields.io/github/license/loootai/looot-skills)](LICENSE) [![Release](https://img.shields.io/github/v/release/loootai/looot-skills)](https://github.com/loootai/looot-skills/releases) [![Docs](https://img.shields.io/badge/docs-docs.looot.ai-12A06A)](https://docs.looot.ai)

21 agent skills that let Claude Code, Cursor, Codex and other agents find emails, enrich companies, pull Google results and more through [looot](https://looot.ai): 4,200+ data API operations from 300+ providers on one prepaid balance.

## Quickstart

1. Install the skills:

   ```bash
   npx skills add loootai/looot-skills
   ```

   OpenClaw, base skill from ClawHub: `openclaw skills install @walidboulanouar/looot`. Pi, all 21 skills plus the MCP server: `pi install npm:pi-looot`.

2. Connect the looot MCP server and sign in with the browser (no key in any file). In Claude Code:

   ```bash
   claude mcp add --transport http looot https://api.looot.ai/mcp
   ```

   then run `/mcp`, pick `looot` and choose Authenticate. Other clients: [looot-mcp](https://github.com/loootai/looot-mcp#install).

3. Ask for a job in plain words, as in the example below.

## Example

Ask your agent:

```text
Use looot to find the work email of Patrick Collison at stripe.com
```

It calls `search` first, which is free. This is the real answer from 2026-11-09, trimmed:

```text
job people.email.find, 29 endpoints
kittai-find-email           Kitt AI        $0.005 per call   works 54% of 12,023 runs, median 4.0 s
companyenrich-people-email  CompanyEnrich  $0.098 per call   no runs yet
fundable-person-email       Fundable       $0.25 per call    no runs yet
```

Then it runs `job:people.email.find` with fallback. looot tries the next provider on a miss and the
result carries the email and the price charged.

## Free to try

Search and inspect are free and need no balance. Paid runs are billed per call at the price
`inspect` shows first, and a failed call costs nothing. A new workspace starts at $0; top up from $5
when you want the first paid result.

## Where it's listed

[![ClawHub](https://img.shields.io/badge/ClawHub-walidboulanouar%2Flooot-12A06A)](https://clawhub.ai/walidboulanouar/looot)
[![skills.sh](https://img.shields.io/badge/skills.sh-loootai%2Flooot--skills-12A06A)](https://skills.sh/loootai/looot-skills)
[![npm pi-looot](https://img.shields.io/npm/v/pi-looot?label=npm%20pi-looot)](https://www.npmjs.com/package/pi-looot)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-ai.looot%2Flooot-12A06A)](https://registry.modelcontextprotocol.io/v0/servers?search=ai.looot/looot)
[![Glama](https://img.shields.io/badge/Glama-looot-12A06A)](https://glama.ai/mcp/connectors/ai.looot/looot)
[![LobeHub](https://img.shields.io/badge/LobeHub-looot-12A06A)](https://lobehub.com/mcp/loootai-looot-mcp)
[![Appside](https://img.shields.io/badge/Appside-looot-12A06A)](https://mcp.appside.build/mcp-servers/looot/)
[![Dify](https://img.shields.io/badge/Dify_Marketplace-looot-12A06A)](https://marketplace.dify.ai/plugins/looot/looot)
[![VS Code Marketplace](https://img.shields.io/badge/VS_Code_Marketplace-looot.looot-007ACC)](https://marketplace.visualstudio.com/items?itemName=looot.looot)

Also on [cursor.directory](https://cursor.directory/plugins/looot).

## Install options

`npx skills add` uses the [skills CLI](https://github.com/vercel-labs/skills) and installs into Claude Code, Cursor, Codex and the other agents it supports. Add `--list` to see the skills first, or `--skill looot-google-serp` to install one. The full setup guide is https://looot.ai/skill.md (the `looot` skill in this repo covers the same ground).

See also: [awesome-looot-use-cases](https://github.com/loootai/awesome-looot-use-cases) (copy-paste recipes) and [awesome-gtm](https://github.com/loootai/awesome-gtm) (open-source GTM tools).

## Skills

`looot` is the base skill: connect the MCP server, sign in, search, inspect, run. The rest are single jobs. They are the same files looot publishes at https://looot.ai/agent-skills.

| Skill | What it does |
| --- | --- |
| `looot` | Base skill: connect the MCP server, search the catalog, read prices, run endpoints with fallback. |
| `looot-ai-search-visibility` | Check AI search visibility |
| `looot-amazon-product` | Look up an Amazon product |
| `looot-backlink-checker` | Check a domain's backlinks |
| `looot-company-email-format` | Find a company's email format |
| `looot-company-list-builder` | Build a company list |
| `looot-domain-keywords` | Find the keywords a domain ranks for |
| `looot-email-verification` | Verify an email address |
| `looot-enrich-a-company` | Enrich a company |
| `looot-enrich-a-person` | Enrich a person |
| `looot-find-phone-numbers` | Find a phone number |
| `looot-find-professional-emails` | Find a professional email |
| `looot-google-maps-reviews` | Read Google Maps reviews |
| `looot-google-serp` | Read a Google results page |
| `looot-job-postings` | Search job postings |
| `looot-keyword-volume` | Check keyword volume and CPC |
| `looot-local-business-search` | Find local businesses |
| `looot-meta-ads-library` | Read a company's Meta ads |
| `looot-reddit-search` | Search Reddit |
| `looot-tiktok-search` | Search TikTok |
| `looot-youtube-transcript` | Get a YouTube transcript |

## License

MIT. See [LICENSE](LICENSE).
