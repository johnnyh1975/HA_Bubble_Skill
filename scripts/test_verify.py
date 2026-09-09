#!/usr/bin/env python3
"""
test_verify.py — negative tests for verify.py.

A checker that passes on a clean tree proves nothing; it also passes if it
does nothing. Each test injects one defect into a throwaway copy of the
library and asserts that verify.py reports it.

Every case below corresponds to a bug that actually shipped at least once, so
a failure here means a real regression in the guard rails.

Usage:
    python3 test_verify.py          # exit 0 = all guards work
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # skill root, one level up


def run_verify(tree: Path):
    proc = subprocess.run([sys.executable, "scripts/verify.py"], cwd=tree,
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def edit(tree: Path, rel: str, old: str, new: str):
    path = tree / rel
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise AssertionError(f"fixture text not found in {rel}: {old[:60]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# Each case: (name, mutate(tree), expected check name in the output)
CASES = []


def case(name, expect):
    def deco(fn):
        CASES.append((name, fn, expect))
        return fn
    return deco


@case("broken anchor reference", "anchors")
def _(tree):
    edit(tree, "SKILL.md", "dashboard-system.md#native-first",
         "dashboard-system.md#no-such-anchor")


@case("invalid YAML in the theme", "yaml")
def _(tree):
    p = tree / "theme" / "Casa5HeyneV2.yaml"
    p.write_text(p.read_text(encoding="utf-8") + "\n  : : broken\n", encoding="utf-8")


@case("theme light/dark asymmetry", "theme-symmetry")
def _(tree):
    edit(tree, "theme/Casa5HeyneV2.yaml",
         '      mush-rgb-teal:         "0, 150, 136"',
         '      mush-rgb-teal-typo:    "0, 150, 136"')


@case("nonexistent Mushroom variable", "banned-vars")
def _(tree):
    edit(tree, "references/mushroom-theme-ref.md",
         "mush-rgb-state-fan:          \"var(--mush-rgb-green)\"",
         "mush-rgb-state-switch: \"var(--mush-rgb-blue)\"")


@case("hardcoded hex in card YAML", "iron-law")
def _(tree):
    edit(tree, "references/bubble-card-ref.md",
         "card_type: calendar",
         "card_type: calendar\n    color: '#D9BE8B'")


@case("version strings disagree", "versions")
def _(tree):
    edit(tree, "references/test-dashboard.yaml", "skill v1.6", "skill v9.9")


@case("stale duplicated metadata comment", "frontmatter")
def _(tree):
    edit(tree, "SKILL.md",
         '  mushroom: "5.2.2"           # verified against Mushroom source',
         '  mushroom: "5.2.2"   # verified   # stale claim from an old edit')


@case("SKILL.md name not kebab-case", "skill-spec")
def _(tree):
    edit(tree, "SKILL.md", "name: ha-bubble-dashboard", "name: HA_Bubble_Dashboard")


@case("angle brackets in description", "skill-spec")
def _(tree):
    edit(tree, "SKILL.md", "TRIGGERS: Bubble Card", "TRIGGERS: <b>Bubble Card</b>")


@case("card type unreachable from the process tree", "routing")
def _(tree):
    edit(tree, "SKILL.md",
         "bubble-card-ref.md#calendar — colour NAMES, never hex",
         "(route removed)")


def run_budget(tree: Path):
    proc = subprocess.run([sys.executable, "scripts/token_budget.py", "--check"],
                          cwd=tree, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def test_budget_guard():
    """token_budget.py must fail when SKILL.md blows past its budget."""
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "skill"
        shutil.copytree(ROOT, tree,
                        ignore=shutil.ignore_patterns("__pycache__", ".git"))
        skill = tree / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\n\n"
                         + ("filler " * 4000), encoding="utf-8")
        rc, out = run_budget(tree)
        if rc == 0:
            return "token_budget.py did not flag an oversized SKILL.md"
        if "over the" not in out:
            return f"unexpected budget output: {out[:120]}"
    return None


def main():
    baseline_rc, baseline_out = run_verify(ROOT)
    if baseline_rc != 0:
        print("The library itself does not pass verify.py — fix that first:\n")
        print(baseline_out)
        return 1

    failures = []
    for name, mutate, expect in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            tree = Path(tmp) / "skill"
            shutil.copytree(ROOT, tree,
                            ignore=shutil.ignore_patterns("__pycache__", ".git"))
            try:
                mutate(tree)
            except AssertionError as e:
                failures.append((name, f"fixture out of date: {e}"))
                continue
            rc, out = run_verify(tree)
            if rc == 0:
                failures.append((name, "verify.py did not flag the injected defect"))
            elif f"[{expect}]" not in out:
                found = re.findall(r"^\[([\w-]+)\]", out, re.M)
                failures.append((name,
                                 f"flagged as {found or 'nothing'}, expected [{expect}]"))

    budget_problem = test_budget_guard()
    total = len(CASES) + 1
    if budget_problem:
        failures.append(("token budget guard", budget_problem))

    print(f"{total - len(failures)}/{total} guards working")
    for name, why in failures:
        print(f"  FAIL  {name}: {why}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
