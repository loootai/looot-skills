"""Adds the same cost line and "Powered by" link to every paid job skill.

Run from the repo root: python3 scripts/add-paid-footer.py
Safe to run twice: a skill that already has the footer is left alone.
"""
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent
UTM = "https://looot.ai/?utm_source=github&utm_medium=skill&utm_campaign=looot-skills&utm_content={name}"
FOOTER = """
## Cost per run

Cost per run: searching and inspecting are free. The run itself needs credit at the price `looot inspect` shows. looot has no trial credit, so the first paid run needs a top-up of $5 minimum.

Powered by [looot]({url})
"""
FREE_MARK = "Cost per run: $0"

changed, skipped = [], []
for skill in sorted((root / "skills").glob("looot-*/SKILL.md")):
    name = skill.parent.name
    text = skill.read_text()
    if FREE_MARK in text:
        continue  # a free skill, it carries its own cost line
    if "## Cost per run" in text:
        skipped.append(name)
        continue
    skill.write_text(text.rstrip("\n") + "\n" + FOOTER.format(url=UTM.format(name=name)))
    changed.append(name)

print(f"added footer to {len(changed)} paid skills, {len(skipped)} already had it")
sys.exit(0)
