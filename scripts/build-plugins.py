"""Builds the Codex plugin's skills from the Claude Code plugin's skills.

plugins/claude-code/looot/skills/ is the one source. Codex reads the Agent Skills format, so each
copy keeps only `name` and `description` in its frontmatter, and the Claude Code slash-command
wording becomes Codex wording.

  python3 scripts/build-plugins.py           rewrite plugins/codex/looot/skills/
  python3 scripts/build-plugins.py --check   exit 1 if the Codex skills are stale
  python3 scripts/build-plugins.py --zip     also write dist/looot-codex-<version>.zip
"""
import json, pathlib, re, shutil, sys, zipfile

root = pathlib.Path(__file__).resolve().parent.parent
src = root / "plugins/claude-code/looot/skills"
codex = root / "plugins/codex/looot"
dst = codex / "skills"

# Claude Code only wording, and what Codex users see instead.
REPLACE = [
    ("$ARGUMENTS", "the job the person asked for"),
    ("Amount asked for, if any: the job the person asked for", "Amount asked for, if any: the amount the person gave"),
    ("`/looot:setup`", "the `setup` skill"),
    ("`/looot:find`", "the `find` skill"),
    ("`/looot:balance`", "the `balance` skill"),
    ("Do not call `run` from this command.", "Do not call `run` from this skill."),
]


def to_codex(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit("skill without frontmatter")
    keep = [l for l in m.group(1).splitlines() if l.startswith(("name:", "description:"))]
    body = text[m.end():]
    for a, b in REPLACE:
        body = body.replace(a, b)
    return "---\n" + "\n".join(keep) + "\n---\n" + body


def expected() -> dict:
    return {p.relative_to(src).as_posix(): to_codex(p.read_text()) for p in sorted(src.glob("*/SKILL.md"))}


def main() -> int:
    want = expected()
    if "--check" in sys.argv:
        have = {p.relative_to(dst).as_posix(): p.read_text() for p in sorted(dst.glob("**/*")) if p.is_file()}
        if have != want:
            print("plugins/codex/looot/skills is stale: run python3 scripts/build-plugins.py")
            return 1
        print(f"codex skills in sync: {len(want)}")
        return 0
    shutil.rmtree(dst, ignore_errors=True)
    for rel, text in want.items():
        (dst / rel).parent.mkdir(parents=True, exist_ok=True)
        (dst / rel).write_text(text)
    print(f"wrote {len(want)} codex skills")
    if "--zip" in sys.argv:
        version = json.loads((codex / "plugin.json").read_text())["version"]
        out = root / "dist" / f"looot-codex-{version}.zip"
        out.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(codex.rglob("*")):
                if f.is_file() and f.name != ".DS_Store":
                    z.write(f, f.relative_to(codex).as_posix())
        print(f"wrote {out.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
