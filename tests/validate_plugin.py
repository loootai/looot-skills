"""Checks the plugin layout and the skill files.

Two plugins: looot-skills (the repo root, all 31 skills) and looot (plugins/claude-code/looot,
the MCP server, the core skill and three commands), plus the Codex copy of looot in
plugins/codex/looot, whose skills must match scripts/build-plugins.py and whose listing must fit
the OpenAI submission limits.

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
    if p["source"] == "./" and plugin_skills != repo_skills:
        errors.append(f"plugin {p['name']} ships {len(plugin_skills)} skills, the repo has {len(repo_skills)}")
    if p["source"] != "./":
        for s in skills_dir.glob("*/SKILL.md"):
            if not re.match(r"^---\nname: " + re.escape(s.parent.name) + r"\ndescription: .+\n", s.read_text()):
                errors.append(f"{s.relative_to(root)}: frontmatter needs name {s.parent.name} then description")
        if not (folder / "README.md").exists() or not (folder / "LICENSE").exists():
            errors.append(f"plugin {p['name']} needs its own README.md and LICENSE (the directory submits the folder)")
        if plugin.get("icon") and not (folder / plugin["icon"]).exists():
            errors.append(f"plugin {p['name']} icon {plugin['icon']} is missing")

# Codex plugin: marketplace entry, manifest limits from the OpenAI submission page, assets, skills in sync
cx_market = json.loads((root / ".agents/plugins/marketplace.json").read_text())
for p in cx_market["plugins"]:
    if "category" not in p:
        errors.append(f"codex marketplace entry {p['name']} needs a category")
    folder = root / p["source"]["path"]
    cx = json.loads((folder / "plugin.json").read_text())
    if cx.get("name") != p["name"]:
        errors.append(f"codex plugin.json name {cx.get('name')} differs from its marketplace entry {p['name']}")
    claude_version = json.loads((root / "plugins/claude-code/looot/.claude-plugin/plugin.json").read_text())["version"]
    if cx.get("version") != claude_version:
        errors.append("codex and claude-code plugin versions differ")
    ui = cx["extensions"]["com.openai"]["interface"]
    for key, most in [("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)]:
        if not ui.get(key) or len(ui[key]) > most:
            errors.append(f"codex interface.{key} is missing or longer than {most}")
    if len(ui.get("defaultPrompt", [])) > 3 or any(len(x) > 128 for x in ui.get("defaultPrompt", [])):
        errors.append("codex interface.defaultPrompt: at most 3 prompts of 128 characters")
    for key in ["websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"]:
        if not str(ui.get(key, "")).startswith("https://"):
            errors.append(f"codex interface.{key} must be an https URL")
    for key in ["logo", "composerIcon"]:
        img = folder / ui.get(key, "missing")
        if not img.exists():
            errors.append(f"codex interface.{key} file is missing")
            continue
        head = img.read_bytes()[:24]
        w, h = int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")
        if head[:8] != b"\x89PNG\r\n\x1a\n" or w != h or w < 48 or w > 4096:
            errors.append(f"codex interface.{key} must be a square PNG between 48 and 4096 px")
    mcp_text = (folder / "mcp.json").read_text()
    if "https://api.looot.ai/mcp" not in mcp_text or "streamable-http" not in mcp_text:
        errors.append("codex mcp.json must be the looot MCP over streamable-http")
    if "headers" in mcp_text or "Bearer" in mcp_text:
        errors.append("codex mcp.json must not carry headers or a token")
import subprocess
if subprocess.run([sys.executable, str(root / "scripts/build-plugins.py"), "--check"], capture_output=True).returncode:
    errors.append("plugins/codex/looot/skills is stale: run python3 scripts/build-plugins.py")

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
    if ".git" in f.parts or "results" in f.parts or "dist" in f.parts or not f.is_file() or f.suffix not in {".md", ".txt", ".json", ".py", ".sh"}:
        continue
    t = f.read_text()
    if chr(0x2014) in t: errors.append(f"em dash in {f.relative_to(root)}")
    if f.suffix == ".json" and "@" in t and "email" in t: errors.append(f"email field left in {f.relative_to(root)}")

print("\n".join(errors) or f"plugin layout ok: {len(repo_skills)} skills, {len(free)} free, {len(paid)} paid")
sys.exit(1 if errors else 0)
