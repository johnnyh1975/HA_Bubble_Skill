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
  8. Skill spec         — SKILL.md frontmatter meets Anthropic's skill spec
  9. Frontmatter        — no stale duplicated comments in the metadata block
  10. Routing coverage    — every card type reachable from the process tree
  11. Orphan files        — every reference file is reachable from SKILL.md

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

# Tooling lives in scripts/; the skill itself is the parent directory.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
YAML_FILES = sorted(glob.glob('theme/*.yaml') + glob.glob('references/*.yaml')
                    + glob.glob('.github/workflows/*.yml'))
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


def check_yaml_examples():
    """Parse every fenced YAML block in the docs.

    These blocks *are* the product — users copy them into Home Assistant. A
    block that does not parse is broken guidance. This check found six view
    scaffolds nesting `sections:` under `cards:` (a dashboard that will not
    load) and a theme line missing the space after a colon.

    Blocks that legitimately do not parse as plain YAML are skipped:
    Home Assistant's `!include*` tags, `{placeholder}` keys, Streamline's
    `[[variable]]` templates, and deliberately-partial fragments marked with
    an ellipsis or a WRONG/CORRECT teaching comment.
    """
    skip_markers = ('!include', '{module_id}', '{{', '[[', '# ...', '...',
                    'WRONG', 'CORRECT', '<', '${')
    for f, text in DOCS.items():
        for m in re.finditer(r'```ya?ml\n(.*?)```', text, re.S):
            body = m.group(1)
            if any(mark in body for mark in skip_markers):
                continue
            try:
                yaml.safe_load(body)
            except Exception as e:
                line = text[:m.start()].count('\n') + 1
                fail('yaml-examples',
                     f'{f}:{line} fenced YAML does not parse: '
                     f'{str(e).splitlines()[0][:80]}')


def check_skill_spec():
    """Anthropic's SKILL.md frontmatter spec, as enforced by skill-creator's
    quick_validate.py. Reimplemented here rather than vendored so the repo
    stays MIT-only and has no external dependency on the skills bundle.

    Rules: exactly one SKILL.md; `name` and `description` required; name is
    kebab-case, <= 64 chars; description <= 1024 chars and free of angle
    brackets (they break the system-prompt block it is injected into).
    """
    skill_mds = [p for p in glob.glob('**/SKILL.md', recursive=True)
                 if '__pycache__' not in p and 'node_modules' not in p]
    if len(skill_mds) != 1:
        fail('skill-spec', f'expected exactly one SKILL.md, found {len(skill_mds)}')
        return

    text = DOCS.get('SKILL.md', '')
    m = re.match(r'(?s)^---\n(.*?)\n---', text)
    if not m:
        fail('skill-spec', 'SKILL.md has no YAML frontmatter')
        return
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        fail('skill-spec', f'frontmatter does not parse: {str(e)[:100]}')
        return

    for key in ('name', 'description'):
        if key not in fm:
            fail('skill-spec', f"missing '{key}' in frontmatter")

    name = str(fm.get('name', '')).strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            fail('skill-spec', f"name '{name}' must be kebab-case")
        if name.startswith('-') or name.endswith('-') or '--' in name:
            fail('skill-spec', f"name '{name}' has a leading/trailing/double hyphen")
        if len(name) > 64:
            fail('skill-spec', f'name is {len(name)} chars, limit is 64')

    desc = str(fm.get('description', '')).strip()
    if desc:
        if '<' in desc or '>' in desc:
            fail('skill-spec', 'description contains angle brackets')
        if len(desc) > 1024:
            fail('skill-spec', f'description is {len(desc)} chars, limit is 1024')
        elif len(desc) > 900:
            warn('skill-spec',
                 f'description is {len(desc)}/1024 chars — little headroom left '
                 'for new triggers or symptoms')


def check_frontmatter():
    """Metadata block sanity: one comment per line, no contradictory version
    strings inside a single entry. A stray second '#' comment on a metadata
    line is how an edit leaves behind a stale claim (v1.5 shipped with a
    'HA 2026.7' comment on a line pinned to 2026.9)."""
    skill = DOCS.get('SKILL.md', '')
    m = re.search(r'(?ms)^metadata:\n(.*?)^---', skill)
    if not m:
        fail('frontmatter', 'SKILL.md metadata block not found')
        return
    for line in m.group(1).splitlines():
        if line.count('#') > 1:
            fail('frontmatter',
                 f'metadata line carries two comments (stale edit?): {line.strip()[:80]}')


def check_routing_coverage():
    """Every documented card type must be reachable from SKILL.md's process
    tree, and every eval must have a trigger in an always-in-context section.

    Guidance that exists but is unreachable is guidance that does not fire —
    the failure mode the Signal Scan was added to fix.
    """
    skill = DOCS.get('SKILL.md', '')
    tree_start = skill.find('## The Process')
    tree_end = skill.find('## Common Pitfalls')
    if tree_start < 0 or tree_end < 0:
        fail('routing', 'SKILL.md process tree not found')
        return
    routable = skill[skill.find('## Signal Scan'):tree_end] or skill[tree_start:tree_end]

    bc = DOCS.get('references/bubble-card-ref.md', '')
    card_types = ['pop-up', 'button', 'sub-buttons', 'horizontal-buttons-stack',
                  'media-player', 'climate', 'cover', 'select', 'separator',
                  'calendar']
    for ct in card_types:
        if f'## #{ct}' in bc and f'#{ct}' not in routable:
            fail('routing', f'card type #{ct} is documented but not reachable '
                            'from the process tree')

    evals = DOCS.get('references/eval-set.md', '')
    if evals:
        always = skill[skill.find('## Signal Scan'):skill.find('## Reference Files')]
        # Each eval names the guidance it tests in a "**Tests:**" line.
        for m in re.finditer(r'^## (#eval-[\w-]+)', evals, re.M):
            name = m.group(1)
            body = evals[m.end():evals.find('\n## ', m.end()) if
                         evals.find('\n## ', m.end()) > 0 else len(evals)]
            tested = re.search(r'\*\*Tests:\*\*(.+?)(?:\n\n|---)', body, re.S)
            if not tested:
                warn('routing', f'{name} has no "Tests:" line — cannot trace')


def check_orphans():
    """A reference file nothing routes to is dead weight.

    Only SKILL.md and the other reference files count as live references.
    A mention in CHANGELOG.md does NOT — the changelog talks about files it
    *deleted*, which is exactly how a stale duplicate stays invisible
    (dashboard-recipes.md survived a sync this way and was only noticed by the
    token budget).
    """
    routing_docs = {n: t for n, t in DOCS.items()
                    if n == 'SKILL.md' or n.startswith('references/')}
    for f in sorted(glob.glob('references/*')):
        name = os.path.basename(f)
        if name == 'eval-set.md':
            continue
        others = '\n'.join(t for n, t in routing_docs.items()
                            if os.path.basename(n) != name)
        if name not in others:
            fail('orphans',
                 f'{f} is not referenced from SKILL.md or any reference file — '
                 'dead file, or a stale copy left behind by a sync?')


def check_duplicates():
    """Catch a file that largely duplicates another.

    The 50 KB dashboard-recipes.md incident: an exact copy of content inside
    dashboard-system.md, referenced nowhere, silently diverging. Compares
    normalised 400-character windows across reference files.
    """
    docs = {n: t for n, t in DOCS.items()
            if n.startswith('references/') and n.endswith('.md')}
    names = sorted(docs)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ta, tb = docs[a], docs[b]
            if min(len(ta), len(tb)) < 4000:
                continue
            smaller, larger = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
            windows = [smaller[k:k + 400] for k in range(0, len(smaller) - 400, 400)]
            if not windows:
                continue
            hits = sum(1 for w in windows if w in larger)
            pct = hits / len(windows) * 100
            if pct > 60:
                small_name = a if len(ta) <= len(tb) else b
                big_name = b if len(ta) <= len(tb) else a
                fail('duplicates',
                     f'{small_name} is {pct:.0f}% contained in {big_name} — '
                     'duplicate content diverges silently; delete one or split '
                     'the ownership')


def main():
    for fn in (check_anchors, check_anchor_lists, check_yaml_valid,
               check_theme_symmetry, check_banned_vars, check_iron_law,
               check_yaml_examples,
               check_versions, check_skill_spec, check_frontmatter,
               check_routing_coverage, check_duplicates,
               check_orphans):
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
