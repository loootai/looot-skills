"""Checks the plugin layout and the skill files.

Every marketplace entry must point at a plugin folder with a manifest, a token-free
MCP config and the repo's skills. The plugin is the repo root (source "./"), so the
one skills/ folder ships as is, with no copy and no symlink. Every skill needs name and description frontmatter.
Free skills need the sections the README promises, paid skills the cost line, and
every skill the "Powered by" link with its own UTM.
Run from anywhere: python3 tests/validate_plugin.py
"""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []
UTM = "https://looot.ai/?utm_source=github&utm_medium=skill&utm_campaign=looot-skills&utm_content={}"

# Marketplace and plugin folders
market = json.loads((root / ".claude-plugin/marketplace.json").read_text())
if market.get("name") != "looot-skills":
    errors.append("marketplace name must be looot-skills, the install command uses it")
repo_skills = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
for p in market["plugins"]:
    folder = root / p["source"]
    manifest = folder / ".claude-plugin/plugin.json"
    if not manifest.exists():
        errors.append(f"missing plugin.json in {p['source']}")
        continue
    plugin = json.loads(manifest.read_text())
    if plugin.get("name") != p["name"]:
        errors.append(f"plugin.json name {plugin.get('name')} differs from marketplace entry {p['name']}")
    if plugin.get("version") != p.get("version"):
        errors.append(f"version differs between marketplace.json and plugin.json for {p['name']}")
    # The MCP server sits inline in plugin.json (a root .mcp.json would also prompt
    # anyone who opens this repo in Claude Code), or in the plugin's .mcp.json.
    mcp_file = folder / ".mcp.json"
    mcp_text = mcp_file.read_text() if mcp_file.exists() else json.dumps(plugin.get("mcpServers", {}))
    if "https://api.looot.ai/mcp" not in mcp_text:
        errors.append(".mcp.json does not point at the looot MCP")
    if "Authorization" in mcp_text or "Bearer" in mcp_text:
        errors.append(".mcp.json must not carry a token")
    skills_dir = folder / "skills"
    if skills_dir.is_symlink():
        errors.append(f"{skills_dir.relative_to(root)} is a symlink: an installed plugin is copied to a cache and the link breaks")
    plugin_skills = sorted(s.parent.name for s in skills_dir.glob("*/SKILL.md"))
    if plugin_skills != repo_skills:
        errors.append(f"plugin {p['name']} ships {len(plugin_skills)} skills, the repo has {len(repo_skills)}")

# Skill files
free, paid = [], []
for name in repo_skills:
    text = (root / "skills" / name / "SKILL.md").read_text()
    m = re.match(r"^---\nname: (.+)\ndescription: (.+)\n---\n", text)
    if not m:
        errors.append(f"{name}: frontmatter needs name then description")
        continue
    if m.group(1).strip() != name:
        errors.append(f"{name}: frontmatter name is {m.group(1).strip()}")
    if name == "looot":
        continue  # the base skill
    if UTM.format(name) not in text:
        errors.append(f"{name}: missing the Powered by link with utm_content={name}")
    if "Cost per run: $0 (free, no top-up needed)" in text:
        free.append(name)
        for need in ["## Setup", "npm install -g looot@", "claude mcp add --transport http looot https://api.looot.ai/mcp",
                     "looot inspect ", "looot run ", "## Example output", "## Next step", "needs a $5 top-up",
                     "## Manual fallback", "Powered by [looot]"]:
            if need not in text:
                errors.append(f"{name}: free skill is missing {need!r}")
    elif "Cost per run: searching and inspecting are free." in text and "$5 minimum" in text:
        paid.append(name)
    else:
        errors.append(f"{name}: no cost line")

if len(free) != 10: errors.append(f"expected 10 free skills, found {len(free)}")
if len(paid) != 20: errors.append(f"expected 20 paid skills, found {len(paid)}")

# Repo-wide text rules
for f in root.rglob("*"):
    if ".git" in f.parts or not f.is_file() or f.suffix not in {".md", ".txt", ".json", ".py", ".sh"}:
        continue
    t = f.read_text()
    if chr(0x2014) in t: errors.append(f"em dash in {f.relative_to(root)}")
    if f.suffix == ".json" and "@" in t and "email" in t: errors.append(f"email field left in {f.relative_to(root)}")

print("\n".join(errors) or f"plugin layout ok: {len(repo_skills)} skills, {len(free)} free, {len(paid)} paid")
sys.exit(1 if errors else 0)
