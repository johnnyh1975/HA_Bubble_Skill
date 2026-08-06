#!/usr/bin/env python3
"""
verify.py — structural self-check for the ha-bubble-dashboard skill library.

Run from the skill root:  python3 verify.py

Checks that have caught real bugs in past releases:
  1. Anchor integrity    — every `file.md#anchor` reference resolves
  2. Anchor list sync    — SKILL.md's per-file anchor lists match reality
  3. YAML validity       — every shipped .yaml parses
  4. Theme mode symmetry — light and dark define the same mush-rgb-* keys
  5. Banned variables    — no non-existent component variables generated
  6. Iron Law            — no hardcoded hex in example YAML outside the theme
  7. Version consistency — one version string across all metadata
  8. Orphan files        — every reference file is reachable from SKILL.md

Exit code 0 = clean, 1 = findings. No third-party dependencies beyond PyYAML.
"""

import re
import sys
import glob
import os

try:
    import yaml
except ImportError:
    print("PyYAML required:  pip install pyyaml")
    sys.exit(2)

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

findings = []
warnings = []


def fail(check, msg):
    findings.append((check, msg))


def warn(check, msg):
    """Not necessarily wrong — curation choices land here. Reported, not fatal."""
    warnings.append((check, msg))

MD = ['SKILL.md', 'README.md', 'CHANGELOG.md', 'available-skills-entry.md'] \
     + sorted(glob.glob('references/*.md'))
MD = [f for f in MD if os.path.exists(f)]
YAML_FILES = sorted(glob.glob('theme/*.yaml') + glob.glob('references/*.yaml'))
DOCS = {f: open(f, encoding='utf-8').read() for f in MD}

# Variables that do not exist in the upstream components. Generating them is
# silently ineffective, which makes them expensive to debug downstream.
# Verified against Mushroom 5.2.2 src/utils/theme.ts.
BANNED_VARS = {
    'mush-rgb-primary':
        'no such variable in Mushroom — wire accent-color-rgb into a state var',
    'mush-rgb-state-switch':
        'no such variable — switches follow mush-rgb-state-entity',
    'mush-rgb-state-update-off':
        'correct name is mush-rgb-update-off (no "state-" segment)',
    'mush-rgb-state-update-installing':
        'correct name is mush-rgb-update-installing (no "state-" segment)',
}
# Lines that *describe* a banned variable rather than generating it.
NEGATION = ('does not exist', 'do not exist', 'no such', 'there is no', 'nonexistent',
            'never did', 'not exist', 'No "', 'no "', 'No `', 'no `',
            'remove them', 'Removed', 'correct name', 'has no effect',
            'no dedicated variable', 'Generating', 'BANNED_VARS')


def anchors_of(text):
    return set(re.findall(r'^## (#[\w-]+)', text, re.M))


def check_anchors():
    defined = {os.path.basename(f): anchors_of(t) for f, t in DOCS.items()}
    for f, t in DOCS.items():
        for m in re.finditer(r'([\w-]+\.md)#([\w-]+)', t):
            target, anchor = m.group(1), '#' + m.group(2)
            if target in defined and anchor not in defined[target]:
                fail('anchors', f'{f} → {target}{anchor} does not resolve')


def check_anchor_lists():
    """SKILL.md lists anchors per reference file; they must still exist."""
    defined = {os.path.basename(f): anchors_of(t) for f, t in DOCS.items()}
    skill = DOCS.get('SKILL.md', '')
    for block in re.finditer(r'\*\*([\w-]+\.md)\*\*[^\n]*\n((?:`#[^\n]*\n)+)', skill):
        fname = block.group(1)
        if fname not in defined:
            continue
        listed = set(re.findall(r'`(#[\w-]+)`', block.group(2)))
        for a in listed - defined[fname]:
            fail('anchor-lists', f'SKILL.md lists {fname}{a}, which does not exist')
        for a in defined[fname] - listed:
            warn('anchor-lists', f'SKILL.md anchor list for {fname} omits {a}')


def check_yaml_valid():
    for f in YAML_FILES:
        try:
            yaml.safe_load(open(f, encoding='utf-8'))
        except Exception as e:
            fail('yaml', f'{f} does not parse: {str(e)[:120]}')


def check_theme_symmetry():
    """A mush-rgb-* key set in only one mode silently falls back to Mushroom
    defaults in the other — invisible until someone switches theme mode."""
    for f in glob.glob('theme/*.yaml'):
        try:
            theme = list(yaml.safe_load(open(f, encoding='utf-8')).values())[0]
        except Exception:
            continue
        modes = theme.get('modes', {})
        if not {'light', 'dark'} <= set(modes):
            continue
        light = {k for k in modes['light'] if k.startswith('mush-rgb')}
        dark = {k for k in modes['dark'] if k.startswith('mush-rgb')}
        for k in sorted(light - dark):
            fail('theme-symmetry', f'{f}: {k} set in light but not dark')
        for k in sorted(dark - light):
            fail('theme-symmetry', f'{f}: {k} set in dark but not light')


def check_banned_vars():
    targets = list(DOCS.items()) + [
        (f, open(f, encoding='utf-8').read()) for f in YAML_FILES]
    for f, text in targets:
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            for var, why in BANNED_VARS.items():
                if var not in line:
                    continue
                # A negation can wrap across lines in prose — look at the
                # surrounding window, not just the hit line.
                window = ' '.join(lines[max(0, i - 4):i + 2])
                if any(k in window for k in NEGATION):
                    continue
                fail('banned-vars', f'{f}:{i} uses `{var}` — {why}')


def check_iron_law():
    """No hardcoded hex in *card* YAML.

    Theme YAML is exempt by definition — a palette recipe is literal colour
    values, that is its whole job. The Iron Law is about card configs, which
    must reference theme variables instead. So only fenced blocks that look
    like card YAML are checked.
    """
    hex_re = re.compile(r'(color|colour)\s*:\s*["\']?#[0-9a-fA-F]{3,8}')
    card_markers = ('custom:bubble-card', 'card_type:', 'custom:mushroom',
                    'type: custom:', 'sub_button:')
    for f, text in DOCS.items():
        lines = text.splitlines()
        block, start = [], 0
        in_block = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                if in_block:
                    body = '\n'.join(block)
                    if any(m in body for m in card_markers):
                        for off, bl in enumerate(block):
                            if bl.strip().startswith('#'):
                                continue
                            if hex_re.search(bl):
                                fail('iron-law',
                                     f'{f}:{start + off} hardcoded hex in card '
                                     f'YAML: {bl.strip()[:70]}')
                    block, in_block = [], False
                else:
                    in_block, start = True, i + 1
                continue
            if in_block:
                block.append(line)


def check_versions():
    """One version of truth across metadata, README and the test dashboard."""
    versions = {}
    m = re.search(r'^\s*version:\s*([\d.]+)', DOCS.get('SKILL.md', ''), re.M)
    if m:
        versions['SKILL.md'] = m.group(1)
    m = re.search(r'Current:\s*\*\*v([\d.]+)\*\*', DOCS.get('README.md', ''))
    if m:
        versions['README.md'] = m.group(1)
    td = 'references/test-dashboard.yaml'
    if os.path.exists(td):
        m = re.search(r'skill v([\d.]+)', open(td, encoding='utf-8').read())
        if m:
            versions[td] = m.group(1)
    if len(set(versions.values())) > 1:
        fail('versions', f'version strings disagree: {versions}')


def check_orphans():
    """A reference file nothing points to is dead weight (see the
    dashboard-recipes.md incident)."""
    corpus = '\n'.join(DOCS.values())
    for f in sorted(glob.glob('references/*')):
        name = os.path.basename(f)
        # count mentions outside the file itself
        others = '\n'.join(t for k, t in DOCS.items() if os.path.basename(k) != name)
        if name not in others and name not in corpus.replace(DOCS.get(f, ''), ''):
            fail('orphans', f'{f} is referenced nowhere — dead file?')


def main():
    for fn in (check_anchors, check_anchor_lists, check_yaml_valid,
               check_theme_symmetry, check_banned_vars, check_iron_law,
               check_versions, check_orphans):
        fn()

    def report(items, label):
        by_check = {}
        for check, msg in items:
            by_check.setdefault(check, []).append(msg)
        print(f'{len(items)} {label}:\n')
        for check in sorted(by_check):
            print(f'[{check}]')
            for msg in by_check[check]:
                print(f'  - {msg}')
            print()

    if findings:
        report(findings, 'finding(s)')
    if warnings:
        report(warnings, 'warning(s) — review, not necessarily wrong')
    if not findings:
        print(f'OK — {len(MD)} markdown files, {len(YAML_FILES)} YAML files, '
              f'no findings' + (f' ({len(warnings)} warnings).' if warnings else '.'))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
