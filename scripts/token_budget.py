#!/usr/bin/env python3
"""
token_budget.py — measure and guard the skill's token footprint.

Why this exists
---------------
SKILL.md is loaded in full for every request, so its size is a fixed tax on
every session. Reference files are anchor-routed and only cost what is
actually read. Those two facts pull in opposite directions: the library can
grow indefinitely without hurting anyone, while SKILL.md cannot.

Measured on this library, a troubleshooting question spends ~96% of its tokens
on SKILL.md and ~4% on the answer. That is the number this tool protects.

What it measures
----------------
Token counts are *estimated* from character counts, weighted by content type
(prose 3.9 chars/token, fenced code 3.1, table rows 3.4). Expect +/-10% against
a real tokeniser. That is deliberate: no network, no dependency, and the
number that matters here is the trend, not the absolute.

Usage
-----
    python3 token_budget.py               # report
    python3 token_budget.py --check       # CI: exit 1 if a budget is exceeded
    python3 token_budget.py --update      # rewrite the baseline after a change
    python3 token_budget.py --json
"""

import glob
import json
import os
import re
import sys
from pathlib import Path

# Tooling lives in scripts/; the skill itself is the parent directory.
ROOT = Path(__file__).resolve().parent.parent
BASELINE = Path(__file__).resolve().parent / "token-baseline.json"

# --- Budgets -----------------------------------------------------------------
# SKILL.md: the fixed per-session cost. The ceiling is generous enough to allow
# real additions but tight enough that unnoticed creep trips it.
SKILL_BUDGET = 17_000

# A single anchor larger than this defeats the point of anchor routing — you
# are loading half a file to answer one question. Split it into design notes
# plus a separate `-scaffold` anchor, as #view-activity was.
ANCHOR_BUDGET = 3_500

# Growth over the committed baseline that should require a conscious decision
# rather than passing silently.
DRIFT_WARN_PCT = 5.0


def est_tokens(text: str) -> int:
    total, in_fence = 0.0, False
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            total += len(line) / 3.9
            continue
        if in_fence:
            total += len(line) / 3.1
        elif stripped.startswith("|"):
            total += len(line) / 3.4
        else:
            total += len(line) / 3.9
    return int(total)


def runtime_files():
    """Files that can enter a conversation. Release and tooling files cannot,
    so they are excluded — the library may carry them for free."""
    files = ["SKILL.md"]
    files += sorted(f for f in glob.glob("references/*")
                    if os.path.isfile(f) and not f.endswith("eval-set.md"))
    files += sorted(f for f in glob.glob("theme/*") if os.path.isfile(f))
    return files


def anchors_of(path: str):
    text = Path(path).read_text(encoding="utf-8")
    parts = re.split(r"(?m)^(## #[\w-]+)", text)
    return {parts[i].replace("## ", "").strip(): est_tokens(parts[i] + parts[i + 1])
            for i in range(1, len(parts), 2)}


def measure():
    os.chdir(ROOT)
    per_file = {f: est_tokens(Path(f).read_text(encoding="utf-8"))
                for f in runtime_files()}
    per_anchor = {}
    for f in per_file:
        if f.endswith(".md") and f != "SKILL.md":
            for anchor, size in anchors_of(f).items():
                per_anchor[f"{os.path.basename(f)}{anchor}"] = size
    return {
        "skill_md": per_file["SKILL.md"],
        "runtime_total": sum(per_file.values()),
        "files": per_file,
        "anchors": per_anchor,
    }


def load_baseline():
    if BASELINE.exists():
        return json.loads(BASELINE.read_text(encoding="utf-8"))
    return None


def report(now, base, as_json=False):
    oversized = sorted(((a, n) for a, n in now["anchors"].items()
                        if n > ANCHOR_BUDGET), key=lambda x: -x[1])
    findings = []

    if now["skill_md"] > SKILL_BUDGET:
        findings.append(
            f"SKILL.md is {now['skill_md']} tokens, over the {SKILL_BUDGET} budget. "
            "Every session pays this. Move situational guidance into an "
            "anchor-routed reference file — but keep anything that must fire "
            "unprompted (the Iron Law, the Signal Scan) here.")
    for anchor, size in oversized:
        findings.append(
            f"{anchor} is {size} tokens, over the {ANCHOR_BUDGET} anchor budget. "
            "Split it into design notes plus a separate scaffold anchor.")

    drift = None
    if base:
        delta = now["skill_md"] - base["skill_md"]
        pct = (delta / base["skill_md"] * 100) if base["skill_md"] else 0
        drift = (delta, pct)
        if pct > DRIFT_WARN_PCT:
            findings.append(
                f"SKILL.md grew {delta:+d} tokens ({pct:+.1f}%) over the baseline. "
                "If that is intended, run --update to move the baseline.")

    if as_json:
        print(json.dumps({"now": now, "findings": findings,
                          "drift": drift}, indent=2))
        return findings

    print(f"SKILL.md (fixed cost, every session)  {now['skill_md']:>7,}"
          f"  / {SKILL_BUDGET:,} budget")
    if drift:
        print(f"  vs baseline                         {drift[0]:>+7,}"
              f"  ({drift[1]:+.1f}%)")
    print(f"Runtime library total                 {now['runtime_total']:>7,}")
    print()
    print("Largest anchors:")
    for anchor, size in sorted(now["anchors"].items(), key=lambda x: -x[1])[:8]:
        flag = "  OVER" if size > ANCHOR_BUDGET else ""
        print(f"  {size:>6,}  {anchor}{flag}")
    sizes = sorted(now["anchors"].values())
    if sizes:
        print(f"\n{len(sizes)} anchors, median {sizes[len(sizes)//2]:,} tokens")

    if findings:
        print("\nFindings:")
        for f in findings:
            print(f"  - {f}")
    else:
        print("\nWithin budget.")
    return findings


def main():
    now = measure()
    base = load_baseline()

    if "--update" in sys.argv:
        BASELINE.write_text(json.dumps(
            {"skill_md": now["skill_md"], "runtime_total": now["runtime_total"]},
            indent=2) + "\n", encoding="utf-8")
        print(f"Baseline set: SKILL.md {now['skill_md']:,} tokens, "
              f"runtime total {now['runtime_total']:,}.")
        return 0

    findings = report(now, base, as_json="--json" in sys.argv)
    if "--check" in sys.argv:
        return 1 if findings else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
