#!/usr/bin/env python3
"""🧑‍⚖️ Health inspection for the Skillzzeria. Zero dependencies.

  python3 scripts/validate.py          check everything (exit 1 on problems)
  python3 scripts/validate.py --menu   print the menu tables for README.md
"""
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
problems: list[str] = []


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        problems.append(f"{path.relative_to(REPO)}: missing YAML frontmatter")
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if km:
            fm[km.group(1)] = km.group(2).strip().strip('"')
    return fm


def check_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        problems.append(f"{path.relative_to(REPO)}: invalid JSON ({e})")
        return None


def collect():
    items = {"skills": [], "agents": [], "commands": []}
    for plugin in sorted((REPO / "plugins").iterdir()):
        if not plugin.is_dir():
            continue
        pj = plugin / ".claude-plugin" / "plugin.json"
        if not pj.exists():
            problems.append(f"{plugin.relative_to(REPO)}: missing .claude-plugin/plugin.json")
        else:
            data = check_json(pj)
            if data and data.get("name") != plugin.name:
                problems.append(f"{pj.relative_to(REPO)}: name {data.get('name')!r} != folder {plugin.name!r}")

        for skill in sorted((plugin / "skills").glob("*/SKILL.md")):
            fm = frontmatter(skill)
            name = skill.parent.name
            if fm.get("name") != name:
                problems.append(f"{skill.relative_to(REPO)}: name {fm.get('name')!r} != folder {name!r}")
            if len(fm.get("description", "")) < 40:
                problems.append(f"{skill.relative_to(REPO)}: description missing or too short to trigger well")
            body = skill.read_text(encoding="utf-8")
            if re.search(r"__[A-Z]", body):
                problems.append(f"{skill.relative_to(REPO)}: still has __TEMPLATE__ placeholders")
            for ref in set(re.findall(r"`((?:references|assets|scripts)/[\w./-]+)`", body)):
                if not (skill.parent / ref).exists():
                    problems.append(f"{skill.relative_to(REPO)}: references missing file {ref}")
            if re.search(r"/Users/|C:\\\\Users", body):
                problems.append(f"{skill.relative_to(REPO)}: contains an absolute user path")
            items["skills"].append((plugin.name, name, fm.get("description", "")))

        for agent in sorted((plugin / "agents").glob("*.md")):
            fm = frontmatter(agent)
            if fm.get("name") != agent.stem or not fm.get("description"):
                problems.append(f"{agent.relative_to(REPO)}: needs name == filename and a description")
            items["agents"].append((plugin.name, agent.stem, fm.get("description", "")))

        for cmd in sorted((plugin / "commands").glob("*.md")):
            fm = frontmatter(cmd)
            if not fm.get("description"):
                problems.append(f"{cmd.relative_to(REPO)}: needs a description")
            items["commands"].append((plugin.name, cmd.stem, fm.get("description", "")))

    mp = check_json(REPO / ".claude-plugin" / "marketplace.json")
    if mp:
        listed = {p["name"] for p in mp.get("plugins", [])}
        for p in mp.get("plugins", []):
            src = p.get("source")
            if isinstance(src, str) and not (REPO / src).exists():
                problems.append(f"marketplace.json: plugin {p['name']} source {src} does not exist")
            pj = REPO / str(src) / ".claude-plugin" / "plugin.json"
            if isinstance(src, str) and pj.exists():
                v = (check_json(pj) or {}).get("version")
                if p.get("version") and v and p["version"] != v:
                    problems.append(f"marketplace.json: {p['name']} version {p['version']} != plugin.json {v}")
        for plugin in (REPO / "plugins").iterdir():
            if plugin.is_dir() and plugin.name not in listed:
                problems.append(f"plugins/{plugin.name} is not listed in marketplace.json")
    return items


def smoke_tests():
    palette = next(REPO.glob("plugins/*/skills/color-theory/scripts/palette.py"), None)
    if palette:
        r = subprocess.run([sys.executable, "-I", str(palette), "contrast", "#000", "#fff"],
                           capture_output=True, text=True)
        if r.returncode != 0 or "21.00:1" not in r.stdout:
            problems.append("palette.py smoke test failed: " + (r.stderr or r.stdout)[:200])
    for sh in REPO.glob("scripts/*.sh"):
        r = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True)
        if r.returncode != 0:
            problems.append(f"{sh.relative_to(REPO)}: bash syntax error {r.stderr.strip()}")


def menu(items):
    def first_sentence(d):
        return re.split(r"(?<=[.!?])\s", d, maxsplit=1)[0][:140]
    print("| 🍕 Skill | Plugin | What it does |\n|---|---|---|")
    for p, n, d in items["skills"]:
        print(f"| `{n}` | {p} | {first_sentence(d)} |")
    print("\n| 👨‍🍳 Agent | Plugin | What it does |\n|---|---|---|")
    for p, n, d in items["agents"]:
        print(f"| `{n}` | {p} | {first_sentence(d)} |")
    print("\n| 🧾 Command | Plugin | What it does |\n|---|---|---|")
    for p, n, d in items["commands"]:
        print(f"| `/{n}` | {p} | {first_sentence(d)} |")


if __name__ == "__main__":
    items = collect()
    if "--menu" in sys.argv:
        menu(items)
        sys.exit(0)
    smoke_tests()
    counts = {k: len(v) for k, v in items.items()}
    if problems:
        print("❌ Health inspection failed:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"✅ Kitchen is clean — {counts['skills']} skills, {counts['agents']} agents, {counts['commands']} commands")
