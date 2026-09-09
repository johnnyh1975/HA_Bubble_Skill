#!/usr/bin/env python3
"""
check_upstream.py — compare the component pins in SKILL.md against the latest
upstream releases.

Every stale-guidance incident in this skill's history started the same way: a
component shipped a release and nobody noticed for weeks. This turns that into
a scheduled job.

Usage:
    python3 check_upstream.py            # human-readable report
    python3 check_upstream.py --json     # machine-readable, for CI

Exit codes:
    0  every pin current (or only unpinnable components drifted)
    1  at least one pin is behind upstream
    2  could not reach the GitHub API

Set GITHUB_TOKEN in the environment to avoid the 60 req/h anonymous rate limit.
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # skill root, one level up

# metadata key in SKILL.md  ->  (owner/repo, human name)
COMPONENTS = {
    "bubble_card":      ("Clooos/Bubble-Card",                     "Bubble Card"),
    "streamline_card":  ("brunosabot/streamline-card",             "Streamline Card"),
    "sidebar_card":     ("DBuit/sidebar-card",                     "Sidebar Card"),
    "mushroom":         ("piitaya/lovelace-mushroom",              "Mushroom"),
    "advanced_history": ("andyblac/Advanced-History-Integration",  "Advanced History"),
}

# Tracked but not pinned to a comparable version string.
UNPINNABLE = {
    "sgcc": ("cataseven/Statistics-Graph-Chart-Card",
             "Statistics Graph Chart Card",
             "minified bundle — pin is an era, not a version; check manually"),
    "bubble_card_tools": ("Clooos/Bubble-Card", "Bubble Card Tools",
                          "ships inside the Bubble Card repo"),
}


def read_pins():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"(?ms)^metadata:\n(.*?)^---", text)
    if not m:
        print("Could not find the metadata block in SKILL.md", file=sys.stderr)
        sys.exit(2)
    pins = {}
    for line in m.group(1).splitlines():
        mm = re.match(r'\s*([a-z_]+):\s*"?([^"#\s]+)"?', line)
        if mm:
            pins[mm.group(1)] = mm.group(2)
    return pins


def latest_release(repo):
    """Newest release tag, falling back to the newest tag for repos that
    publish tags without GitHub Releases."""
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "ha-bubble-skill-upstream-check"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    for url in (f"https://api.github.com/repos/{repo}/releases/latest",
                f"https://api.github.com/repos/{repo}/tags?per_page=1"):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.load(r)
            if isinstance(data, dict) and data.get("tag_name"):
                return data["tag_name"], data.get("published_at", "")[:10]
            if isinstance(data, list) and data:
                return data[0].get("name", ""), ""
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                raise RuntimeError("GitHub API rate limit — set GITHUB_TOKEN")
            continue
        except Exception:
            continue
    return None, ""


def normalise(v):
    return re.sub(r"^v", "", (v or "").strip())


def main():
    as_json = "--json" in sys.argv
    pins = read_pins()
    rows, behind = [], []

    for key, (repo, label) in COMPONENTS.items():
        pinned = pins.get(key)
        if not pinned:
            rows.append((label, "—", "not pinned", "MISSING"))
            continue
        try:
            latest, date = latest_release(repo)
        except RuntimeError as e:
            print(e, file=sys.stderr)
            sys.exit(2)
        if not latest:
            rows.append((label, pinned, "unknown", "UNREACHABLE"))
            continue
        status = "current" if normalise(latest) == normalise(pinned) else "BEHIND"
        if status == "BEHIND":
            behind.append((label, pinned, normalise(latest), date))
        rows.append((label, pinned, normalise(latest) + (f" ({date})" if date else ""), status))

    for key, (_repo, label, note) in UNPINNABLE.items():
        rows.append((label, pins.get(key, "—"), "manual", note))

    if as_json:
        print(json.dumps({
            "behind": [{"component": b[0], "pinned": b[1],
                        "latest": b[2], "released": b[3]} for b in behind],
            "rows": [{"component": r[0], "pinned": r[1],
                      "latest": r[2], "status": r[3]} for r in rows],
        }, indent=2))
    else:
        width = max(len(r[0]) for r in rows)
        print(f"{'component'.ljust(width)}  {'pinned':<12} {'latest':<24} status")
        print("-" * (width + 48))
        for label, pinned, latest, status in rows:
            print(f"{label.ljust(width)}  {pinned:<12} {latest:<24} {status}")
        if behind:
            print("\nAction needed — scan the source tree, not just the release "
                  "notes:\n")
            for label, pinned, latest, date in behind:
                print(f"  {label}: {pinned} -> {latest}"
                      + (f" (released {date})" if date else ""))
            print("\nSee CHANGELOG.md, 'Standing check', for the per-release "
                  "verification list.")

    return 1 if behind else 0


if __name__ == "__main__":
    sys.exit(main())
