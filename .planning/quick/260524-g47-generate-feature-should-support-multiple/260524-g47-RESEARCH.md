---
quick_id: 260524-g47
type: research
status: complete
---

# Quick Task 260524-g47: Research

**Researched:** 2026-05-24
**Domain:** `cement/ext/ext_generate.py` schema extension (PR #768 follow-up,
GH Issue #779)
**Confidence:** HIGH (all findings file:line-grounded against current HEAD)

## Summary

CONTEXT.md locks the schema. This research is implementation-ready grafting
notes: where each new branch attaches inside `_process_features` (lines
29-102) and the variable loop (lines 139-186), the fixture layout that PR
#768 settled on, the test idioms to mirror, the coverage-gate landmines the
implementer must address by name, and a concrete demo extension that adds
a third feature without disturbing `docker` / `docker_compose`.

**Primary recommendation:** Three logical edit zones, in this order:

1. **Validation pass** (currently lines 35-48): add a third loop that
   enforces the schema-collision rule (Decision A — raise `ValueError` if
   `prompt_mode: select` AND `enabled`/`disabled` co-exist) and validates
   that each `selected` entry has `value:` and that the feature-level
   `default` matches one of those values (Decision D pre-check).
2. **`_resolve` closure** (currently lines 58-84): branch on
   `feature.get('prompt_mode') == 'select'` to render the multi-valued
   prompt + dispatch lookup. `feature_states[name]` is currently `bool`;
   it must widen to `bool | str` (the selected `value`) so the merge step
   downstream can branch on type. Legacy boolean path stays byte-identical.
3. **Merge step** (currently lines 89-102) + **variable loop** (currently
   lines 147-186): on the select path, look up the matched branch in
   `selected` and merge its `ignore`/`exclude`/`variables` with the
   `or []` null-safety pattern (Pitfall A). The variable loop gains a
   pre-prompt short-circuit when `var.get('prompt') is False`, with the
   existing `assert var[key] is not None` at line 150-152 relaxed to
   accept `False` for `prompt` but continue to reject `None`.

## 1. Exact Code-Site Grafting Plan

### Edit zone A — fast-fail validation (after current line 48)

Today, the validation pass is two loops (35-42 build `feature_by_name`,
43-48 verify `requires`). Append a third loop for the new schema:

```python
# pseudo-graft, AFTER line 48
for feature in features:
    mode = feature.get('prompt_mode')
    if mode is None:
        continue                        # legacy boolean — no further checks
    if mode != 'select':
        raise ValueError(
            f"Feature '{feature['name']}' has invalid prompt_mode "
            f"'{mode}' (must be 'select' or omitted)")
    # Decision A: collision check
    if 'enabled' in feature or 'disabled' in feature:
        raise ValueError(
            f"Feature '{feature['name']}' uses prompt_mode: select; "
            f"'enabled'/'disabled' blocks are not allowed in this mode")
    # selected: must be a non-empty list of dicts with value:
    selected = feature.get('selected') or []
    if not selected:
        raise ValueError(
            f"Feature '{feature['name']}' uses prompt_mode: select but "
            f"has no 'selected' branches")
    values: list[str] = []
    for branch in selected:
        if branch.get('value') is None:
            raise ValueError(
                f"Feature '{feature['name']}' has a 'selected' branch "
                f"missing required key: value")
        # Pitfall C: YAML may decode 1 as int; coerce to str for compare
        values.append(str(branch['value']))
    # Decision D pre-check: feature's `default` must be in values
    if feature.get('default') is not None:
        if str(feature['default']) not in values:
            raise ValueError(
                f"Feature '{feature['name']}' default "
                f"'{feature['default']}' is not in selected values "
                f"{values}")
```

This mirrors the existing `raise ValueError(...)` precedent on lines 40-48
(message style `"Feature 'X' ... reason"`) — Decision row in CONTEXT.md
"Error message style". The validation runs **before** any prompt, matching
the up-front discipline at lines 35-48.

### Edit zone B — `_resolve` closure (currently lines 58-84)

The closure today returns `bool`. After the change it returns
`bool | str` — `True`/`False` for boolean features, the matched `value`
string for select features. `feature_states` annotation widens
correspondingly (line 56: `dict[str, bool]` → `dict[str, bool | str]`).
The dispatch site at line 87 (`_resolve(feature['name'])`) is unchanged.

```python
# pseudo-graft, REPLACING lines 69-83
default = feature.get('default')
mode = feature.get('prompt_mode')

if mode == 'select':
    # Decision D: --defaults uses feature's default directly
    if self.app.pargs.defaults:
        # Pre-validated above to be in selected values
        feature_states[name] = str(default)
    else:                                       # pragma: nocover
        # interactive path mirrors the bool prompt block at 76-83
        prompt_text = feature.get('prompt') or \
            f"Select Feature: {name}"
        default_hint = f" [{default}]" if default else ''

        class FeaturePrompt(shell.Prompt):       # pragma: nocover
            class Meta:
                text = f"{prompt_text}{default_hint}:"
        p = FeaturePrompt(auto=False)            # pragma: nocover
        val: str = p.prompt() or str(default)    # pragma: nocover
        # Pitfall D: case normalization BEFORE validate BEFORE lookup
        if feature.get('case') in ['lower', 'upper', 'title']:
            val = getattr(val, feature['case'])()  # pragma: nocover
        if feature.get('validate') is not None:    # pragma: nocover
            assert re.match(feature['validate'], val), \
                f"Invalid Response (must match: " \
                f"'{feature['validate']}')"
        # Decision B: unmatched input → AssertionError
        # (validate may pass but value not in selected; that is a
        # template-author bug)
        valid_values = [str(b['value'])
                        for b in feature.get('selected') or []]
        assert val in valid_values, \
            f"Invalid Response (must be one of: {valid_values})"
        feature_states[name] = val
else:
    # LEGACY boolean path — byte-for-byte unchanged from today's 69-83
    default = bool(feature.get('default', False))
    if self.app.pargs.defaults:
        feature_states[name] = default
    else:
        default_hint = 'Y/n' if default else 'y/N'  # pragma: nocover
        default_val = 'y' if default else 'n'       # pragma: nocover
        class FeaturePrompt(shell.Prompt):           # pragma: nocover
            class Meta:
                text = f"Enable Feature: {name} [{default_hint}]:"
                default = default_val
        p = FeaturePrompt(auto=False)                # pragma: nocover
        val: str = p.prompt() or default_val         # pragma: nocover
        feature_states[name] = val.lower() == 'y'    # pragma: nocover
return feature_states[name]
```

Note: the **legacy interactive branch** carries `# pragma: nocover` today
(lines 73-83) per Phase 03 Plan 07 batch — the new interactive select
branch must match that pragma policy (it is not coverable from the test
suite for the same reason: shell.Prompt blocks under captured stdin). The
**`--defaults` select branch IS coverable** and MUST be covered.

### Edit zone C — merge step (currently lines 89-102)

Today's merge at lines 89-102 uses `block_key = 'enabled' if enabled
else 'disabled'`. Split on the type of `feature_states[name]`:

```python
# pseudo-graft, REPLACING lines 89-102
if 'features' not in data:
    data['features'] = {}
for feature in features:
    name = feature['name']
    state = feature_states[name]
    data['features'][name] = state          # bool OR str — both are fine
                                            # for downstream template use

    if isinstance(state, bool):
        # LEGACY path — unchanged
        block_key = 'enabled' if state else 'disabled'
        block = feature.get(block_key) or {}
    else:
        # NEW select path: find the matched branch by value
        block = {}
        for branch in feature.get('selected') or []:
            if str(branch['value']) == state:
                block = branch
                break
        # Decision B already enforced state ∈ values above, so
        # this loop is guaranteed to set `block`.

    # Pitfall A: `or []` MUST appear inside this select branch too
    vars.extend(block.get('variables') or [])
    exclude_list.extend(block.get('exclude') or [])
    ignore_list.extend(block.get('ignore') or [])
```

Note the last three lines: today's lines 100-102 use
`block.get('variables', [])` (no `or []`). The 6895aa52 fix landed `or []`
only at the **top-level** YAML keys (lines 125-127), not inside
feature blocks. For consistency with Pitfall A and to be null-safe inside
`selected:` branches, switch all three to `or []` here. **This is a
deliberate generalization of the 6895aa52 pattern — flag for the
planner.** Today's `block.get('variables', [])` form is null-unsafe if a
template author writes `enabled: { variables: null }`; the existing test
suite does not exercise that and PR #768 left it alone, so this is a
behavior-aligned tightening, NOT a public-API break.

### Edit zone D — variable loop (currently lines 147-186)

Two surgical edits:

1. **Line 150-152** — current code:
   ```python
   for key in ['name', 'prompt']:
       assert var[key] is not None, \
           f"Required generate config key missing: {key}"
   ```
   The `prompt` half of this assertion must be loosened to accept `False`
   while still rejecting `None`. The cleanest form:
   ```python
   assert var['name'] is not None, \
       "Required generate config key missing: name"
   assert var['prompt'] is not None, \
       "Required generate config key missing: prompt"
   ```
   (Split because `name` rejects `None` only, `prompt` already rejects
   `None`; `False` is a valid value that `is not None` accepts as-is.)

   This is the **lowest-risk change** in the whole task — `is not None`
   semantics already accept `False` correctly. Verify with the existing
   test suite still passing; no fixture changes needed for the legacy
   path.

2. **AFTER the assertion block, BEFORE the prompt logic** — short-circuit
   on `prompt is False`:
   ```python
   if var['prompt'] is False:
       # Silent variable — use default without prompting
       assert var['default'] is not None, \
           f"Variable '{var['name']}' has prompt: false but no default"
       val = var['default']
       # case + validate still apply per CONTEXT.md Decision under
       # 'Silent (no-prompt) variables' → 'Validate / case interaction'
   else:
       # Current lines 154-171 unchanged
       val: Any = None
       if var['default'] is not None and self.app.pargs.defaults:
           val = var['default']
       elif var['default'] is not None:
           default_text = f" [{var['default']}]"
       else:
           default_text = ''   # pragma: nocover  # defensive: unreachable
       if val is None:
           ...
   ```
   Then **lines 173-184 stay byte-for-byte unchanged** — they already
   apply `case` and `validate` to `val` regardless of how `val` was
   produced. This delivers the CONTEXT.md "Validate / case interaction
   on silent vars: reusing it, not branching from it" guarantee for free.

## 2. Test Fixture Layout

PR #768 settled the layout at `tests/data/templates/generate/testN/` —
one directory per scenario, with `.generate.yml` plus the test's content
files (the files that get rendered/excluded/ignored to assert against).
Numbering went up to `test15`; **add new fixtures starting at `test16`**.

Existing feature-related fixtures (for style reference):

| Fixture | Scenario | Used By |
|---------|----------|---------|
| test6 | feature1=true default, feature2=false default — happy path | test_generate_features_enabled |
| test7 | feature1=false, feature2=true — opposite booleans | test_generate_features_disabled |
| test8 | missing `name:` on feature — ValueError | test_generate_features_missing_name |
| test9 | features both true with `requires:` satisfied | test_generate_features_requires_satisfied |
| test10 | feature with `requires: nonexistent` — ValueError | test_generate_features_requires_unknown |
| test11 | feature1=false, feature2 requires feature1 — cascade | test_generate_features_requires_not_satisfied |
| test12 | `enabled:` with null body | test_generate_features_null_block |
| test13 | feature with only `name`/`default`, no blocks | test_generate_features_minimal |
| test14 | three-level transitive requires cascade | test_generate_features_transitive_requires |
| test15 | out-of-order requires (b before a) | test_generate_features_requires_out_of_order |

Content-file convention is descriptive filename equals matchable behavior
— `feature1-only`, `no-feature1`, `feature2-file` etc. — so the assertion
reads like English: `assert exists_join(tmp.dir, 'feature1-only')`.

**Minimum new fixtures for this task (numbered 16..22 for room):**

| New Fixture | Purpose | Content Files |
|-------------|---------|---------------|
| test16 | select-mode happy path, `--defaults` picks branch "2" | take-me, branch-1-only, branch-2-only, branch-N-file |
| test17 | select-mode collision: prompt_mode: select + `enabled:` block — ValueError | take-me (test never executes copy) |
| test18 | select-mode + `validate` regex; fixture is invocation-only; AssertionError on input mismatch is covered by the `--defaults` path using a `default:` not present in `selected` would be REJECTED at validation time, so cover the runtime-unmatched assertion via the interactive path with a mocked `shell.Prompt.prompt` — see Test 4 below | take-me |
| test19 | select-mode with `prompt: false` silent variable, `case: upper` normalization on the feature prompt itself, `--defaults` | take-me, file-rendered-with-silent-var |
| test20 | select-mode with `default:` not in `selected` values — ValueError at config-validation | take-me (never reached) |
| test21 | select-mode with missing `value:` in a branch — ValueError | take-me |
| test22 | top-level `variables` with `prompt: false` (sentinel outside selected, per CONTEXT.md "Silent vars usable outside `selected`") | take-me-silent |

The test count grows by ~7 fixtures; the existing dir layout absorbs this
without restructuring.

## 3. Existing Test-Style Audit

Three representative tests in `tests/ext/test_ext_generate.py` to mirror:

### 3a. `test_generate_features_enabled` (lines 161-187) — happy path

```python
def test_generate_features_enabled(tmp):
    argv = ['generate', 'test6', tmp.dir, '--defaults']
    with GenerateApp(argv=argv) as app:
        app.run()
        assert exists_join(tmp.dir, 'feature1-only')
        assert not exists_join(tmp.dir, 'no-feature1')
        with open(os.path.join(tmp.dir, 'feature1-file')) as f:
            assert 'feature1_val' in f.read()
```

**Idioms:** `argv` list with `--defaults`, context manager around
`GenerateApp(argv=argv)`, `exists_join` helper (defined at line 10) for
file-existence assertions, content assertion via `open().read()` + `in`.

### 3b. `test_generate_features_missing_name` (lines 226-231) — ValueError

```python
def test_generate_features_missing_name(tmp):
    argv = ['generate', 'test8', tmp.dir, '--defaults']
    with GenerateApp(argv=argv) as app:
        with raises(ValueError, match='Required feature config key missing: name'):
            app.run()
```

**Idiom:** `raises(ValueError, match='...')` from `cement.utils.test`, the
match string is a substring/regex of the error. All new schema-validation
tests use this exact shape (with new match strings).

### 3c. `test_no_default` (lines 89-97) — mocked prompt

```python
def test_no_default(tmp):
    with patch.object(shell.Prompt, 'prompt', return_value='Bogus'):
        argv = ['generate', 'test5', tmp.dir]
        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me')) as f:
                assert 'Bogus' in f.read()
```

**Idiom:** `patch.object(shell.Prompt, 'prompt', return_value=...)` to
inject a prompt response without `--defaults`. This is how the unmatched-
input AssertionError test (test18) should fire its runtime path — patch
the prompt to return a value that passes the feature's `validate` regex
but is NOT in `selected` values.

**Coverage caveat:** the interactive feature-prompt path itself (the new
`FeaturePrompt` class for select mode) is marked `# pragma: nocover` for
the same reason today's lines 73-83 are — the prompt class is constructed
inside the closure and `p.prompt()` cannot be reached under captured
stdin. The `--defaults` branch of the select dispatch and the assert
checks for value-in-selected (when run via the `--defaults` path through
the mocked prompt for interactive) are the coverable parts.

## 4. Coverage Gate Landmines

100% line coverage is project-absolute (CLAUDE.md "100% test coverage
required"; PROJECT.md "Quality gates: 100% test coverage ... — all
absolute"). Every new branch must have a named test fixture + invocation:

| # | New Branch | Edit Zone | Test Fixture + Invocation |
|---|-----------|-----------|--------------------------|
| 1 | `if mode is None: continue` (early-out for legacy) | A | Any existing test6..15 invocation exercises this (no new fixture; existing coverage already runs the legacy path through Edit Zone A) |
| 2 | `if mode != 'select': raise ValueError` | A | New: invoke with `prompt_mode: bogus` in test fixture, `raises(ValueError, match="invalid prompt_mode")` |
| 3 | `if 'enabled' in feature or 'disabled' in feature: raise ValueError` (Decision A collision) | A | test17, `raises(ValueError, match="'enabled'/'disabled' blocks are not allowed")` |
| 4 | `if not selected: raise ValueError` | A | Empty `selected: []` fixture, `raises(ValueError, match="no 'selected' branches")` |
| 5 | `if branch.get('value') is None: raise ValueError` | A | test21, `raises(ValueError, match="missing required key: value")` |
| 6 | `if str(feature['default']) not in values: raise ValueError` (Decision D pre-check) | A | test20, `raises(ValueError, match="is not in selected values")` |
| 7 | `if mode == 'select' and pargs.defaults: feature_states[name] = str(default)` | B | test16 with `--defaults`, assert correct branch's files present |
| 8 | Select-mode merge: walk `selected` to find matching `value` and assign `block` | C | test16 with `--defaults` — implicit through file presence/absence assertions |
| 9 | `vars.extend(block.get('variables') or [])` (null-safe inside select branch) | C | test16's chosen branch declares `variables:` to exercise the populated path; a separate fixture with `variables: null` under selected (e.g. test16's "N" branch) exercises the null-coalesce |
| 10 | Variable-loop short-circuit: `if var['prompt'] is False` | D | test19 with `prompt: false` on a variable; assert rendered file contains the default value verbatim |
| 11 | `assert var['default'] is not None` inside silent-var short-circuit (defensive) | D | Either cover with a fixture that has `prompt: false` and no `default`, **or** mark `# pragma: nocover # defensive: unreachable` if uncoverable; CONTEXT.md says raises are testable so cover it — fixture: `raises(AssertionError, match="prompt: false but no default")` |
| 12 | Top-level silent variable (`prompt: false` outside `selected`) | D | test22, assert silent var's default appears in rendered output |
| 13 | Unmatched-input runtime AssertionError (Decision B) | B | Mock `shell.Prompt.prompt` to return a value matching `validate` regex but absent from `selected`; `raises(AssertionError, match="must be one of:")` — pattern from test_no_default (line 89-97) |

**Pragma-able branches** (the new interactive select-mode prompt — the
`FeaturePrompt` class body and `p.prompt()` call): mirror today's
ext_generate.py:73-83 pattern (`# pragma: nocover` — uncoverable under
captured stdin). Locked-vocabulary category is `defensive: unreachable`
per the Phase 03 Plan 07 vocabulary cited in CONTEXT.md.

**Coverage tip:** the existing test_invalid_variable_value (line 80-86)
already proves that variable-loop AssertionErrors are reachable via the
`--defaults` path when `default` violates `validate`. Reuse that idiom
for any new variable-level assertions added in the silent-var branch.

## 5. Demo Extension Shape

The demo today has two features (`docker` boolean default-true,
`docker_compose` boolean default-true requires docker). Add a third
feature using `prompt_mode: select` that composes naturally and
demonstrates a silent variable + ignore patterns.

**Concrete proposal: `web_framework` feature**

```yaml
- name: web_framework
  prompt_mode: select
  prompt: "Web Framework [(N)one/1=Flask/2=FastAPI]"
  validate: "^[N12]$"
  case: upper
  default: "N"
  selected:
    - value: "N"
      ignore:
        - '.*requirements\.txt.*'
        - '.*wsgi\.py.*'
    - value: "1"
      variables:
        - name: framework_name
          prompt: false
          default: "flask"
        - name: framework_version
          prompt: false
          default: "3.0"
      ignore:
        - '.*fastapi.*'
    - value: "2"
      variables:
        - name: framework_name
          prompt: false
          default: "fastapi"
        - name: framework_version
          prompt: false
          default: "0.115"
      ignore:
        - '.*flask.*'
```

**New template files needed** under
`demo/generate-features/templates/generate/webapp/`:

1. `requirements.txt` (Jinja2-templated):
   ```
   {{ framework_name }}=={{ framework_version }}
   ```
2. `wsgi.py` (small Jinja2 stub that imports the chosen framework):
   ```python
   # {{ framework_name }} wsgi entrypoint for {{ project_name }}
   ```

These two files exercise the ignore-when-"N" branch (both ignored when
`web_framework=N`), the silent variables (`framework_name` /
`framework_version` set without prompting under values "1" or "2"), and
they preserve the file-presence asymmetry the existing demo README
illustrates ("With defaults" vs "With X disabled" output trees).

Per CONTEXT.md "Adding-not-replacing — none of the existing demo files
(Dockerfile, app.py, docker-compose.yml, README.md, .dockerignore) are
removed or renamed", the existing `docker` + `docker_compose` boolean
features stay byte-for-byte; this is a third sibling feature in the same
`features:` list.

**Note on `.dockerignore`:** The demo README at line 73 lists
`.dockerignore` as a generated output file, but the directory listing
returned only `Dockerfile`, `app.py`, `docker-compose.yml`, `README.md`
— **no `.dockerignore` file is currently in the demo template dir**.
This is a pre-existing demo gap (the README describes a file that
doesn't ship), unrelated to this task. **Flag for the planner** —
the planner may choose to (a) ignore it, (b) add the missing file as a
zero-cost demo-correctness fix, or (c) update the README to drop the
nonexistent file. Recommend (b): add a minimal `.dockerignore` while
already touching the demo template directory.

**README extension:** Add a new section between "Configuration" and
"What to Expect" titled e.g. **"Multi-Valued Feature (prompt_mode:
select)"** that walks through:

- the new schema keys (`prompt_mode`, `validate`, `case`, `default`,
  `selected`),
- how `case: upper` normalizes user input before lookup,
- the `prompt: false` sentinel and what "silent" means,
- one concrete invocation: `pdm run python myapp.py generate webapp
  /tmp/myproject --defaults` and what file tree it produces with the
  default branch (N → no requirements.txt, no wsgi.py).

Extend the "What to Expect" section with one new example tree showing the
multi-valued branch picked (e.g. `web_framework=1` → Flask).

## 6. Pitfalls

**A. `or []` null-safety inside `selected` branches (Edit Zone C).** The
6895aa52 fix landed `or []` at the **top-level** keys only (current
lines 125-127). Today's enabled/disabled merge at lines 100-102 still
uses `block.get('variables', [])` — null-unsafe if a template author
writes `variables: null` inside a feature block. The new code MUST use
`block.get('variables') or []` (and same for `exclude`, `ignore`) inside
the `selected` branch merge. **Recommendation: generalize the pattern
to the legacy boolean merge at the same time** — a one-line
fix that closes the same null-safety hole and stays within the spirit
of 6895aa52. **Flag for planner adjudication** — it's a behavior
change for an untested edge case, but consistency wins and the existing
test12 fixture proves the null-coalesce is intended at the top level.

**B. Lazy-resolver closure recursion (lines 58-84) and `requires`
cascade.** `_resolve` recurses on `requires` and returns False if any
prereq is False (lines 62-68). For a select-mode feature with `requires`
declared, the same cascade applies — but `feature_states[name]` is no
longer `bool`. When `_resolve` shortcircuits to False (line 67), the
merge step needs to handle `state is False` for a select-mode feature.
**Per CONTEXT.md Decision C "No default branch fallback"**: a
select-mode feature that gets `requires`-disabled should NOT pick any
`selected` branch — its files default to the no-branch state (no
variables, no excludes, no ignores from `selected`). The merge code
above handles this naturally: `isinstance(state, bool) and state is
False` falls into the legacy `block = feature.get('disabled') or {}`
branch, which is empty `{}` because the validation step rejected
`disabled:` co-existing with select-mode. **Verify this by example**:
test fixture where a select-mode feature has `requires: docker` and
docker=False; the select-mode feature's selected branches must all be
skipped.

**C. YAML int-vs-str coercion on numeric `value:` entries.** YAML decodes
unquoted `value: 1` as Python `int(1)`. Quoted `value: "1"` stays a
`str`. User input from `shell.Prompt` is always a `str`. CONTEXT.md
Decision under "selected data shape" → "Value comparison" implies
case-then-compare, but does not pin coercion. **Solution (already
encoded in edit zones A and C above): always `str(branch['value'])`
before comparison and before pre-validating `default`**. This makes
both `value: 1` (unquoted) and `value: "1"` (quoted) behave identically.
The canonical schema example in CONTEXT.md line 198-219 uses quoted
strings (`"N"`, `"1"`, `"2"`) which is the safe form; coercion protects
template authors from accidentally landing the unquoted form.

**D. Case-then-validate-then-lookup ordering** (Edit Zone B, the new
interactive select prompt). The existing variable loop applies `case`
first (line 173-180), then `validate` (line 182-184). The new feature-
level prompt MUST follow the same order — case normalizes the input,
then validate enforces the regex, then dispatch looks up the matched
`value` in `selected`. CONTEXT.md explicitly pins this ("the same
case-then-validate ordering already used for variables at
ext_generate.py:173-184"). **The interactive branch carries
`# pragma: nocover`, so this ordering is verified through the
`--defaults` path indirectly + by inspection. Recommend: encode the
ordering in a code comment so reviewers can audit it.**

**E. `--defaults` and `default` consistency** (Decision D). When
`--defaults` is set and the feature is select-mode, the feature's
`default` must already be in `selected` values (validated at config
time per row 6 of the coverage table). After validation, the
`--defaults` branch trusts that and does `feature_states[name] =
str(default)` directly. **Pitfall: the existing feature `default` for
boolean features at line 69 is `bool(feature.get('default', False))`
— the new select-mode default is `str`, not `bool`. The
`bool(...)` coercion at line 69 must remain inside the legacy branch
only.** The edit zone B graft above respects this by branching on
`mode == 'select'` BEFORE the `bool(...)` coercion.

**F. Pre-existing demo README inconsistency.** README lists
`.dockerignore` (line 73) as a generated file but the demo template
directory doesn't ship one. Not caused by this task, but the planner
may want to add it as a zero-cost fix while editing the demo. See
section 5 above.

## 7. Compatibility Verification

Walking each in-tree `.generate.yml` against the proposed code:

- `demo/generate-features/templates/generate/webapp/.generate.yml` —
  has no `prompt_mode:` key on either feature; legacy boolean path
  selected at Edit Zone B; merge at Edit Zone C falls into the
  `isinstance(state, bool)` branch. **Unchanged behavior** ✓
- `tests/data/templates/generate/test1..test5/.generate.yml` — no
  `features:` at all (or non-feature variants); the `features` check
  at line 134-135 skips `_process_features` entirely. **Unchanged
  behavior** ✓
- `tests/data/templates/generate/test6..test15/.generate.yml` — all
  use boolean features with `enabled:`/`disabled:` blocks; no
  `prompt_mode:` key. Same path as the demo. **Unchanged behavior** ✓
- `tests/data/templates/generate/test8/.generate.yml` — missing
  `name:` on feature; hits the existing ValueError at line 39-41
  BEFORE the new validation pass runs. **Unchanged error message,
  unchanged ValueError class** ✓
- `tests/data/templates/generate/test12/.generate.yml` — `enabled:`
  with null body; the existing `feature.get(block_key) or {}` at
  line 98 already null-coalesces. The new merge code preserves this
  in the legacy branch. **Unchanged behavior** ✓

**Pitfall A flagged elsewhere is the one real behavior generalization**
— current `block.get('variables', [])` at line 100-102 vs proposed
`block.get('variables') or []`. The existing test12 fixture proves
that null block-bodies work (`enabled: null` → empty `{}` → empty
`[]`), so this generalization is consistent with existing tests. If
the planner wants zero-risk, scope it to the **new** `selected`
branch merge only and leave the legacy lines 100-102 untouched.
**Author recommendation: tighten both — one trivial diff, one
consistency win, zero observable change in the existing test
matrix.**

The variable loop change (line 150 assertion split + `prompt is False`
short-circuit) is **additive only**: every existing fixture has
`prompt:` as a non-None string, which passes `is not None` and falls
into the else-branch with byte-identical behavior. **Unchanged
behavior on all legacy paths** ✓

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `feature_states` annotation can widen from `dict[str, bool]` to `dict[str, bool \| str]` without mypy complaints elsewhere in the module | §1 Edit Zone B | mypy gate fails; would need an explicit `cast` or local var-name change; trivial fix at planning time |
| A2 | The interactive feature-prompt path for select mode is uncoverable under captured stdin (mirrors today's `# pragma: nocover` on lines 73-83) | §1 Edit Zone B | If actually coverable via Prompt-mock the way variables are, the test surface grows by 1-2 tests but no behavior change |
| A3 | Generalizing `block.get('variables', [])` → `block.get('variables') or []` at lines 100-102 is acceptable as a consistency fix and is not a public-API break | §1 Edit Zone C / §6 Pitfall A | Planner may scope it to the new code only — see §6 recommendation |
| A4 | Adding `.dockerignore` to the demo template directory (closing the pre-existing README inconsistency) is acceptable scope creep for this task | §5 / §6 Pitfall F | Planner may defer to a separate doc-only quick task; zero impact on the schema work |
| A5 | The unmatched-input runtime AssertionError can be exercised via `patch.object(shell.Prompt, 'prompt', return_value=...)` (same idiom as test_no_default at lines 89-97), even though the surrounding code carries `# pragma: nocover` | §3c / §4 row 13 | If the surrounding pragma blocks the mock from reaching the assertion line, the assert must move outside the pragma'd block OR be exercised via a different vector (e.g. the `--defaults` path with a default that is in `selected` but case-normalization produces a different value — but Decision D's validation rejects that at config time). Mitigation: structure the `assert val in valid_values` line OUTSIDE the no-cover pragma block so coverage tracks it. |

## Open Questions

None. All decisions are locked by CONTEXT.md; the three "Flag for
planner" items (Pitfall A scope, .dockerignore demo fix, Assumption A5
pragma placement) are explicit planner-adjudication callouts, not open
research questions.

## Sources

### Primary (HIGH confidence)
- `cement/ext/ext_generate.py` HEAD — lines 29-186 read in full
- `tests/ext/test_ext_generate.py` HEAD — all 22 test functions reviewed
- `tests/data/templates/generate/test{1..15}/.generate.yml` — fixture
  layout enumerated; test6/7/8/9/10/12/13/15 read in full
- `demo/generate-features/templates/generate/webapp/.generate.yml` and
  the four content files (Dockerfile, app.py, docker-compose.yml,
  README.md) — read in full
- `demo/generate-features/README.md` — read in full
- `demo/generate-features/myapp.py` — read in full to confirm
  template-app wiring shape
- `.planning/quick/260524-g47-generate-feature-should-support-multiple/260524-g47-CONTEXT.md`
  — read in full (locks the schema; this research operates within those
  locks)
- `.planning/PROJECT.md` — Cement 3 backward-compat + 100% coverage
  constraints confirmed
- `/Users/derks/Development/DFL/cement/CLAUDE.md` — Conventional Commits,
  78-char wrap, ruff/mypy gates confirmed

### Secondary (MEDIUM confidence)
- Recent commit log: 6895aa52 (null-safe top-level `or []`) and
  d9b83ff8 (lazy-prompt features via recursive resolver) — cited in
  CONTEXT.md and verified consistent with the current line numbering
  in ext_generate.py

### Tertiary (LOW confidence)
- None. All claims are backed by file:line evidence in HEAD.

## Metadata

**Confidence breakdown:**
- Code-site grafting plan: HIGH — every line cited against HEAD
- Test fixture layout: HIGH — `find` enumerated the directory, content
  files inspected
- Test-style audit: HIGH — three test functions quoted verbatim
- Coverage gate landmines: HIGH — every new branch has a named fixture
  + invocation; pragma-able branches are explicitly called out with
  locked-vocabulary category
- Demo extension shape: HIGH — concrete YAML + concrete file proposals
- Pitfalls: HIGH — every pitfall grounded in a file:line citation
- Compatibility verification: HIGH — every in-tree `.generate.yml`
  walked against the proposed code

**Research date:** 2026-05-24
**Valid until:** 2026-06-23 (30 days; the schema is locked and HEAD is
the target — no fast-moving externals)
