#!/usr/bin/env python3
"""Agent vault check. Plain script, no AI. Reads only; changes nothing.

    python3 vault-check.py [vault folder]

Reports: links to notes that do not exist, notes missing owner/type/status/updated,
notes nothing links to (outside state/, inbox/, archive/), iCloud duplicate copies, and files that look like
they hold a key or password (file name only, never the text).
"""
import os, re, sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), ".."))
REQUIRED = ("owner", "type", "status", "updated")
NO_ORPHAN_CHECK = ("state/", "inbox/", "archive/", "tools/")
ROOT_NOTES = {"CLAUDE.md", "AGENTS.md", "VAULT.md"}
SECRET = re.compile(r"AIza[0-9A-Za-z_-]{10,}|\bsk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|ntn_[A-Za-z0-9]{20,}|xox[bpoa]-|"
                    r"Bearer [A-Za-z0-9._-]{20,}|Basic [A-Za-z0-9+/=]{20,}|\b(?=[A-Za-z0-9 ]*\d)(?=[A-Za-z0-9 ]*[A-Z])[A-Za-z0-9]{4}( [A-Za-z0-9]{4}){5}\b")
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")

def notes():
    for d, _, files in os.walk(ROOT):
        for f in files:
            if f.endswith(".md"):
                yield os.path.relpath(os.path.join(d, f), ROOT)

def frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    return {l.split(":", 1)[0].strip() for l in text[4:end].splitlines() if ":" in l}

def main():
    paths = sorted(notes())
    by_name = {}
    for p in paths:
        by_name.setdefault(os.path.basename(p)[:-3].lower(), []).append(p)
    by_path = {p[:-3].lower(): p for p in paths}
    broken, missing, secrets, inbound = [], [], [], {p: 0 for p in paths}
    for p in paths:
        text = open(os.path.join(ROOT, p), encoding="utf-8", errors="replace").read()
        keys = frontmatter(text)
        lacking = [k for k in REQUIRED if k not in keys]
        if lacking:
            missing.append((p, lacking))
        if SECRET.search(text):
            secrets.append(p)
        for target in LINK.findall(text):
            t = target.strip().lower().removesuffix(".md")
            hit = by_path.get(t) or (by_name.get(t, [None])[0])
            if not hit and os.path.exists(os.path.join(ROOT, target.strip())):
                continue  # link to a non-note file, such as a .base view
            if hit:
                inbound[hit] += 1
            else:
                broken.append((p, target))
    dupes = [p for p in paths if re.search(r" \d+\.md$", p) and re.sub(r" \d+\.md$", ".md", p) in inbound]
    orphans = [p for p, n in inbound.items() if n == 0 and p not in ROOT_NOTES
               and not p.startswith(NO_ORPHAN_CHECK) and os.path.basename(p) != "README.md"]
    print(f"Agent vault check - {len(paths)} notes in {ROOT}")
    print(f"\nLinks to notes that do not exist: {len(broken)}")
    for p, t in broken: print(f"  {p} -> [[{t}]]")
    print(f"\nNotes missing frontmatter fields: {len(missing)}")
    for p, l in missing: print(f"  {p}: missing {', '.join(l)}")
    print(f"\nNotes nothing links to: {len(orphans)}")
    for p in orphans: print(f"  {p}")
    print(f"\nPossible iCloud duplicate copies: {len(dupes)}")
    for p in dupes: print(f"  {p}")
    print(f"\nFiles that may hold a key or password (check by hand, never paste the text): {len(secrets)}")
    for p in secrets: print(f"  {p}")
    return 1 if (broken or missing or secrets or dupes) else 0

if __name__ == "__main__":
    sys.exit(main())
