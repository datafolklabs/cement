---
created: 2026-05-08T03:51:47.860Z
title: Analyze and resolve GitHub issue #777
area: core
files:
  - cement/core/foundation.py:1488-1499
  - tests/core/test_foundation.py
github_issue: https://github.com/datafolklabs/cement/issues/777
related_pr: https://github.com/datafolklabs/cement/pull/760
---

## Problem

The `extensions` config-override block in `cement/core/foundation.py:1488-1499`
guards against `self._meta.config_section` but reads/writes via `label`
(= `self._meta.label`). This silently fails when an app explicitly sets
`Meta.config_section` to a value other than `Meta.label`:

```python
if 'extensions' in self.config.keys(self._meta.config_section):  # config_section
    exts = self.config.get(label, 'extensions')                  # label  ← mismatch
    ...
    self.config.set(label, 'extensions', ext_list)               # label  ← mismatch
```

In the common case (`Meta.config_section is None` → defaults to `Meta.label`)
there is no observable bug. The divergence only fires when an app customizes
`config_section` independently.

Discovered during cross-AI review of PR #760 (template_dirs config-override).
The new `template_dirs` block was fixed to use `self._meta.config_section`
consistently — this todo tracks the parallel fix for the pre-existing
`extensions` block, which was deliberately scoped out of #760 to keep that PR
minimal.

## Solution

Mirror the fix already applied to `template_dirs` in PR #760:

```diff
 if 'extensions' in self.config.keys(self._meta.config_section):
-    exts = self.config.get(label, 'extensions')
+    exts = self.config.get(self._meta.config_section, 'extensions')
     ...
-    self.config.set(label, 'extensions', ext_list)
+    self.config.set(self._meta.config_section, 'extensions', ext_list)
```

Add a regression test that customizes `Meta.config_section != Meta.label`
and asserts extensions defined in the divergent section are loaded.

**Pickup order:** wait until #760 is merged so the two fixes don't conflict
in `_setup_config_handler`. After merge, this is `/gsd-quick`-sized — single
file edit + one new test, ~5-10 LOC.

**Acceptance:**
- [ ] `extensions` config-override normalises against `Meta.config_section`
- [ ] Regression test for `config_section != label` case
- [ ] `make test && make comply` green, 100% coverage held
- [ ] No BC change for the common case (`config_section is None`)
