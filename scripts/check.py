#!/usr/bin/env python3
"""THE PRE-WRITE GATE. Run this BEFORE writing a note, not after.

    VAULT_DIR=/path/to/vault LIBRARY_DIR=/path/to/library python3 check.py "PERMIT-12345"
    python3 check.py "term one" "term two"

WHY IT EXISTS
On 27 August 2026 a session was handed two jobs marked blocking. Both had
already been done - a permit's monitoring reports on 5 August, a securities
filing on 29 July. Nobody had searched `Documents/` for the permit number or the
form name first. That was the sixth such re-derivation.

The vault's own search tool is the reason the habit never stuck: it returns
"Total results: 0" on its first call every single time, so a session searches,
sees nothing, and believes it. **This script does not use that tool.** It reads
the files directly, and it is deliberately noisy about what it finds.

WHAT IT SEARCHES
Every vault note, +ANSWERED, +NUMBERS, the filenames in the source library, and - since
8 October 2026 - the names of files HIDDEN INSIDE library PDFs (email attachments carried
as file-attachment annotations, embedded files, portfolio items), from _attachments.py's
index. Added after a records request asked a state agency for a spreadsheet it had already
produced inside a PDF portfolio. Run `python3 _attachments.py --scan --new` to refresh.
Case-insensitive substring, plus a loose variant that ignores spaces, hyphens
and underscores so `PERMIT-12345`, `PERMIT 12345` and `permit12345` all match.

WHAT TO DO WITH THE ANSWER
If it prints anything at all under EXISTING WORK, open those notes before you
write. A hit is not proof the work is complete, but writing without reading
them is how this vault loses a session.
"""
import os
import re
import sys
from collections import defaultdict

VAULT = os.environ.get("VAULT_DIR", os.path.expanduser("~/vault"))
LIBRARY = os.environ.get("LIBRARY_DIR", os.path.expanduser("~/library"))
LIB_ROOTS = [""]  # search the whole library folder
# "_archive" added 7 September 2026. Anything in a folder called _archive is a frozen,
# superseded copy kept only for recovery. The gate exists to answer "is this already in
# the vault?", and a stale duplicate answering yes is worse than no answer - this vault's
# documented fault is corrections being made where they are noticed and not everywhere
# they live. Archived copies must not come back as hits.
SKIP = {".git", ".obsidian", ".smart-env", "node_modules", "__pycache__", "mapenv",
        "_archive"}
# Files the tooling writes about itself. A hit ONLY here means nobody has
# actually written anything - see the _manifest.py self-reference note.
SELF_WRITTEN = {
    "+READ MANIFEST - what has been fully read.md",
    "Hot cache.md",
    "_MANIFEST - campaign folder vs vault coverage.md",
}
PRIORITY = ["+ANSWERED", "+NUMBERS", "Findings", "Documents", "Analyses",
            "People and Entities", "Records Requests", "Claims", "Decisions"]


def loose(s):
    return re.sub(r"[\s\-_.]", "", s).lower()


def rank(rel):
    for i, p in enumerate(PRIORITY):
        if rel.startswith(p):
            return i
    return len(PRIORITY)


def hidden(term):
    """files hidden inside library PDFs whose names match, from _attachments-index.json"""
    import json
    ix = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_attachments-index.json")
    if not os.path.exists(ix):
        return []
    tl, tloose = term.lower(), loose(term)
    out = []
    for r in json.load(open(ix)).get("rows", []):
        n = r.get("name", "")
        if tl in n.lower() or (len(tloose) > 4 and tloose in loose(n)):
            out.append(r)
    return out


def search(term):
    tl, tloose = term.lower(), loose(term)
    real, selfonly, lib = defaultdict(list), [], []

    for dp, dn, fns in os.walk(VAULT):
        dn[:] = [d for d in dn if d not in SKIP]
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dp, fn), VAULT)
            try:
                text = open(os.path.join(dp, fn), encoding="utf-8",
                            errors="replace").read()
            except OSError:
                continue
            hits = []
            for i, line in enumerate(text.split("\n"), 1):
                if tl in line.lower() or (len(tloose) > 4 and tloose in loose(line)):
                    hits.append((i, line.strip()[:150]))
            if not hits and tl not in fn.lower():
                continue
            if fn in SELF_WRITTEN:
                selfonly.append(rel)
            else:
                real[rel] = hits

    for root in LIB_ROOTS:
        base = os.path.join(LIBRARY, root)
        for dp, dn, fns in os.walk(base):
            dn[:] = [d for d in dn if d not in SKIP]
            for fn in fns:
                if tl in fn.lower() or (len(tloose) > 4 and tloose in loose(fn)):
                    lib.append(os.path.relpath(os.path.join(dp, fn), LIBRARY))
    return real, selfonly, lib


def report(term):
    real, selfonly, lib = search(term)
    hid = hidden(term)
    print("=" * 72)
    print(f"  {term}")
    print("=" * 72)

    if hid:
        print(f"\n  HIDDEN INSIDE LIBRARY PDFs - {len(hid)} file(s) match. THE RECORD MAY ALREADY BE IN HAND.")
        print("  Do not request it until you have opened these:")
        for r in hid[:15]:
            where = r["pdf"] + (f"  >  {r['item']}" if r.get("item") else "")
            state = ("extracted: " + r["in_hand"]) if r.get("in_hand") else "NOT EXTRACTED - python3 _attachments.py --extract \"" + r["pdf"] + "\""
            print(f"      {r['name']}  ({r['how']})")
            print(f"          in {where}")
            print(f"          {state}")
        if len(hid) > 15:
            print(f"      ...and {len(hid) - 15} more")
        print()

    if not real and not lib and not hid:
        print("\n  NOTHING FOUND. This subject appears to be genuinely new.")
        if selfonly:
            print(f"  (named in {len(selfonly)} generated file(s) only, which is not coverage)")
        print()
        return 0

    if real:
        total = sum(len(v) for v in real.values())
        print(f"\n  STOP. {len(real)} note(s) already mention this, {total} line(s).")
        print("  Open them before you write anything.\n")
        for rel in sorted(real, key=lambda r: (rank(r), r)):
            print(f"  {rel}")
            for ln, txt in real[rel][:3]:
                print(f"      L{ln}: {txt}")
            if len(real[rel]) > 3:
                print(f"      ...and {len(real[rel]) - 3} more line(s)")
        print()

    if selfonly:
        print(f"  Named ONLY in {len(selfonly)} tooling-generated file(s) - "
              f"that is NOT coverage:")
        for rel in selfonly:
            print(f"      {rel}")
        print()

    if lib:
        print(f"  {len(lib)} source file(s) in the library match this string:")
        for rel in sorted(lib)[:25]:
            print(f"      {rel}")
        if len(lib) > 25:
            print(f"      ...and {len(lib) - 25} more")
        print()
    return len(real) + len(hid)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    hits = sum(report(t) for t in sys.argv[1:])
    print("=" * 72)
    print("  Existing work found. Read it first." if hits
          else "  Clear. Nothing in the vault covers these terms yet.")
