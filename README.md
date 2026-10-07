# looot skills

Agent skills for [looot](https://looot.ai): one key and one prepaid balance for 2,500+ data API endpoints from 90+ providers. Each folder under `skills/` is one skill in the [Agent Skills](https://agentskills.io) format (`SKILL.md` with `name` and `description` frontmatter). The agent searches the catalog, sees the price before it runs, and pays per call. A failed call costs nothing. Top up from $5.

## Install

```bash
npx skills add loootai/looot-skills
```

That uses the [skills CLI](https://github.com/vercel-labs/skills) and installs into Claude Code, Cursor, Codex and the other agents it supports. Add `--list` to see the skills first, or `--skill looot-google-serp` to install one.

Then set looot up once: https://looot.ai/skill.md (the `looot` skill in this repo covers the same ground).

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

## Cost

The skill files are free. Searching and inspecting are free. A run is billed per call at the price `looot inspect` shows first.

## License

MIT. See [LICENSE](LICENSE).
