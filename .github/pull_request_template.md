## What changed

<!-- One or two sentences. Link an issue if there is one. -->

## Checklist

- [ ] `python3 verify.py` passes
- [ ] `python3 test_verify.py` passes (if `verify.py` changed)
- [ ] `CHANGELOG.md` updated under the current unreleased version
- [ ] Component facts came from the **source tree**, not release notes or
      editor schemas alone — editor-only scans have missed YAML-facing
      options twice
- [ ] New guidance is reachable: routed from the Signal Scan or the process
      tree in `SKILL.md`, not only present in a reference file
- [ ] No hardcoded hex in card YAML examples (the Iron Law)
- [ ] New component options are version-gated if they need a minimum release
