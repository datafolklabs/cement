# Phase 5: Deprecations, Docs & Security Stubs - Pattern Map

**Mapped:** 2026-05-07
**Files analyzed:** 12 (1 new + 11 modified)
**Analogs found:** 12 / 12 (every file has a concrete in-repo analog —
either its own current-state block, a repo-root sibling markdown, an
existing AUDIT POINT comment in `pyproject.toml`, or a sibling commit
recipe in `CHANGELOG.md`)

> **Phase character:** Doc-only. There is **one** new file
> (`DEPRECATIONS.md`); everything else is in-place edits to existing
> files. Patterns are mostly markdown shape, RST conventions, the
> Conventional Commits + 78-char wrap commit recipe, and the
> CHANGELOG bucket conventions from CLAUDE.md §"Changelog Maintenance".
> No application architecture changes; no new tests; no new make
> targets (the existing `docs:` target is modified, not added).
>
> The planner consumes this file as: "for each file, here is the exact
> current text, the exact target shape, the closest in-repo precedent
> for that shape, and the pitfalls already pre-identified in
> RESEARCH.md so the executor doesn't trip on them." Per RESEARCH.md
> Pitfalls 1-8, the planner should encode `read_first` requirements
> on `docs/source/conf.py` (Pitfall 2 — duplicate dict),
> `.planning/codebase/CONVENTIONS.md` line 35 (Pitfall 6 — already
> mostly done), and the bucket-per-commit table (Pitfall 7 — drop
> planning-artifact entries).

## File Classification

| File | Role | Data Flow / Concern | Closest Analog | Match Quality |
|------|------|---------------------|----------------|---------------|
| `cement/core/deprecations.py` | registry edit (source code, runtime warning text) | declarative dict literal | self — current lines 4-9 | exact (in-place value swap, 2 of 4 entries) |
| `cement/ext/ext_logging.py:140-151` (`set_level` docstring) | docstring sweep (RST autodoc, deprecation note) | docstring prose + RST inline-literal | self — current lines 146-147; sibling docstring at `cement/core/foundation.py:608` already in v3.2.0 form | exact (in-place prose swap) |
| `cement/ext/ext_logging.py:364-383` (`fatal()` docstring) | docstring sweep (RST autodoc, deprecation note) | docstring prose + RST inline-literal | self — current lines 368-369; sibling `set_level` docstring above (same change) | exact (in-place prose swap) |
| `cement/ext/ext_smtp.py:116-158` (`send()` docstring) | docstring sweep (add `.. deprecated::` admonition) | RST directive insertion | self — current lines 140-143 (Returns block); RST `.. deprecated::` directive is a Sphinx built-in | role-match (no prior `.. deprecated::` admonition exists in repo; the directive itself is canonical Sphinx) |
| `cement/utils/shell.py:35-39` (`cmd()` docstring) | docstring sweep (RST inline-literal fix) | docutils RST parser | self — current lines 35-39; sibling `exec_cmd()` docstring at lines 86-91 carries the **same** prose pattern (NOT in scope per CONTEXT.md D-08 #4) | exact (single-token swap `/` → `or`) |
| `cement/core/interface.py:102` (`InterfaceManager.list`) | source-code edit (autodoc workaround, string-quote return annotation) | autodoc method-name shadow | sibling pattern in `cement/core/{hook,handler,extension}.py` uses `import builtins` + `builtins.list[T]`. CONTEXT.md D-08 #3 picks **string-quote** instead (no audit-baseline rebase). | partial (sibling-different by design — D-08 #3 explicitly picks string-quote over the sibling form; rationale captured in RESEARCH.md Open Question 1) |
| `docs/source/conf.py` (drop duplicate `html_theme_options`) | sphinx config edit | Python module-scope assignment | self — lines 19-33 (kept) vs lines 51-53 (deleted) | exact (block delete; the line-19 dict already carries the correct shape) |
| `docs/source/index.rst` and/or `docs/source/api/index.rst` (toctree wiring) | RST toctree edit | sphinx document graph | self — `docs/source/index.rst` lines 8-13 is the live toctree that already references `api/core/index`, `api/utils/index`, `api/ext/index`. `api/index.rst` is the orphan duplicate. | exact (delete orphan OR add `:hidden:` reference; planner picks per RESEARCH.md Pitfall 4 recommendation = option (a) delete) |
| `Makefile` (`docs:` target) | Makefile gate edit (build flag + AUDIT POINT) | declarative recipe | self — current lines 62-66; AUDIT POINT comment **shape** mirrors `pyproject.toml:68-71, 79-82, 102-145` (Phase 2 D-12 + D-10/D-11 + Phase 3 D-08 D-06 precedent) | exact (in-place flag insertion + AUDIT POINT comment, mirroring `pyproject.toml`) |
| `README.md` | repo-root markdown refresh | prose + badge link | self — current line 5 (badge) + line 60 (list-item link); siblings `CHANGELOG.md` and `CONTRIBUTORS.md` are no-frontmatter H2-section markdown files | exact (line delete x2) |
| `.github/CONTRIBUTING.md` (Guidelines + new Commit Conventions section) | repo-root markdown refresh | prose | self — current lines 33-80; canonical commit-shape doc is `CLAUDE.md` §"Commit Conventions" (the replacement section anchors on it) | exact (section rewrite + new "Commit Conventions" subsection) |
| `DEPRECATIONS.md` (NEW, repo root) | new repo-root markdown | per-deprecation H2 block format | sibling `CHANGELOG.md` (H2 sections, no frontmatter) + `CONTRIBUTORS.md` (no frontmatter, repo-root markdown). Per-block structure has no in-repo precedent — D-07 establishes it. | role-match (sibling shape is the no-frontmatter H2 markdown convention; per-block structure is **new convention** for this phase) |
| `.planning/codebase/CONVENTIONS.md` (PEP 604/585 ratify line 35 only) | planning intel refresh | prose + ruff config example | self — current line 35 (`target-version = "py39"`); body of "Type annotations" section (lines 22-26, 92-95) **already** in PEP 604/585 form per RESEARCH.md Pitfall 6. Live `pyproject.toml:88` says `target-version = "py310"`. | exact (1-line bump, NOT a wholesale rewrite) |
| `.planning/REQUIREMENTS.md` (SECv2-01..03 expansion) | REQUIREMENTS.md expansion | per-stub multi-line block | self — current lines 91-94 (one-liner stubs) + analog **inside the same file** at `### v1` `SEC-01..03` lines 73-75 (one-liner shape preserved). Phase-shaped scope notes pattern is **new** for this section but mirrors the multi-line shape of `### Release` `REL-01..05` block elsewhere in the doc. | exact (in-place expansion of the first 3 of 4 entries; SECv2-04 untouched) |
| `CHANGELOG.md` (per-commit append) | CHANGELOG entry | one-line bucketed entry | self — `## 3.0.15 - DEVELOPMENT` section already populated with **133+ existing entries** across 5 buckets (`Bugs:`, `Features:`, `Refactoring:`, `Misc:`, `Deprecations:`). Phase 5 appends 11 entries (NOT 14 — see Pitfall 7 in RESEARCH.md). | exact (append to existing buckets, no new section) |

> **Files NOT modified** (tracked here so the planner doesn't
> accidentally include them):
>
> - `cement/core/foundation.py:608` (`framework_logging` docstring
>   already says `v3.2.0` — D-04 explicitly excludes).
> - `cement/utils/shell.py:exec_cmd()` docstring (same RST prose
>   pattern as `cmd()` but NOT in the live warning list — D-08 #4
>   names only `cmd()`; RESEARCH.md Example 5 notes the parallel fix
>   is deferred).
> - `docs/source/*.rst` beyond `index.rst` + `api/index.rst` toctree
>   wiring (sphinx is API-only per D-05; no new RST pages).
> - `SECURITY.md` (out of `SEC-01..03` scope; SECv2-04 is its own
>   future-milestone concern).
> - `tests/core/test_deprecations.py` and `tests/ext/test_ext_smtp.py`
>   (DEPREC-03 already-satisfied; no new test work).

## Pattern Assignments

### `cement/core/deprecations.py` (registry edit, runtime warning text)

**Analog:** self, lines 4-9 (the live `DEPRECATIONS` dict). Two of
four entries already match the target pattern (`3.0.8-1` and
`3.0.8-2` say `"Cement v3.2.0"`). The two non-conforming entries
(`3.0.10-1`, `3.0.16-1`) are the change targets.

**Current state** (`cement/core/deprecations.py:4-9`):

```python
DEPRECATIONS = {
    '3.0.8-1': "Environment variable CEMENT_FRAMEWORK_LOGGING is deprecated in favor of CEMENT_LOG, and will be removed in Cement v3.2.0",  # noqa: E501
    '3.0.8-2': "App.Meta.framework_logging will be changed or removed in Cement v3.2.0",  # noqa: E501
    '3.0.10-1': "The FATAL logging facility is deprecated in favor of CRITICAL, and will be removed in future versions of Cement.",  # noqa: E501
    '3.0.16-1': "SMTPMailHandler.send() returning bool is deprecated. It will return the smtplib senderrs dict in a future version of Cement",  # noqa: E501
}
```

**Target state** (D-02/D-03 — pin both vague messages to v3.2.0):

```python
DEPRECATIONS = {
    '3.0.8-1': "Environment variable CEMENT_FRAMEWORK_LOGGING is deprecated in favor of CEMENT_LOG, and will be removed in Cement v3.2.0",  # noqa: E501
    '3.0.8-2': "App.Meta.framework_logging will be changed or removed in Cement v3.2.0",  # noqa: E501
    '3.0.10-1': "The FATAL logging facility is deprecated in favor of CRITICAL, and will be removed in Cement v3.2.0.",  # noqa: E501
    '3.0.16-1': "SMTPMailHandler.send() returning bool is deprecated. It will return the smtplib senderrs dict in Cement v3.2.0",  # noqa: E501
}
```

**Why mechanical:** Two-line value swap. `3.0.10-1` keeps its
trailing period (the original had one). `3.0.16-1` has no trailing
period (the original didn't). The `# noqa: E501` line-length
suppression stays — the strings remain >100 chars after the swap.
The `deprecate()` helper at line 12-16 is unchanged; the GitBook
URL (`f"...#{deprecation_id}"`) and the dotted-anchor format
(`#3.0.10-1`) are preserved.

**Acceptance grep** (D-18 #5):
```bash
grep -E '"3\.[0-9]+\.[0-9]+-[0-9]+":' cement/core/deprecations.py | wc -l
# expected: 4
grep -cE 'v3\.2\.0' cement/core/deprecations.py
# expected: 4 (one per entry)
```

**Read first:** `cement/core/deprecations.py` (whole file is 17
lines).

**Commit:** `refactor(core.deprecations): tighten removal-version
language` (D-16 step 1; CHANGELOG bucket: `Refactoring:` →
`[core.deprecations] Pin 3.0.10-1 and 3.0.16-1 removal version to
v3.2.0`).

---

### `cement/ext/ext_logging.py:140-151` (set_level docstring)

**Analog:** self, lines 146-147 (the deprecation note in the
`set_level` docstring) + sibling `cement/core/foundation.py:608`
(`framework_logging` docstring, already in `v3.2.0` form — the
target shape).

**Current state** (`cement/ext/ext_logging.py:146-147`):

```python
        As of Cement 3.0.10, the FATAL facility is deprecated and will be
        removed in future versions of Cement. Please us `CRITICAL` instead.
```

**Target state** (D-04):

```python
        As of Cement 3.0.10, the FATAL facility is deprecated and will be
        removed in Cement v3.2.0. Please use ``CRITICAL`` instead.
```

**Three changes (per RESEARCH.md Example 2):**
1. `"future versions of Cement"` → `"Cement v3.2.0"` (the load-bearing
   D-04 change)
2. `"us"` → `"use"` (typo carry-over; in-flight cleanup)
3. Single-backtick `` `CRITICAL` `` → double-backtick
   `` ``CRITICAL`` `` (RST inline-literal — single backticks render
   as emphasis, not inline-literal, in autodoc)

**Why mechanical:** Three unrelated single-token cleanups in adjacent
prose. Changes 2 and 3 are zero-risk; if planner wants strictest
scope, defer them — but they keep the docstring sweep clean and the
follow-up surface honest.

**Read first:** `cement/ext/ext_logging.py` (lines 140-160 — the
`set_level` method) AND `cement/core/foundation.py:608` (the target-
shape docstring; do NOT edit, just confirm shape).

**Commit:** `refactor(ext.logging): tighten FATAL deprecation removal
version in docstrings` (D-16 step 2; this commit also covers the
`fatal()` docstring below — same file, same change pattern, same
commit).

---

### `cement/ext/ext_logging.py:364-383` (fatal() docstring)

**Analog:** self, lines 368-369. **Same change pattern** as
`set_level` above — folded into the same commit.

**Current state** (`cement/ext/ext_logging.py:368-369`):

```python
        As of Cement 3.0.10, this method is deprecated and will be removed in
        future versions of Cement. Please us `critical()` instead.
```

**Target state** (D-04):

```python
        As of Cement 3.0.10, this method is deprecated and will be removed in
        Cement v3.2.0. Please use ``critical()`` instead.
```

**Why mechanical:** Identical three-token swap as `set_level`. Both
docstrings ship in one commit (single `[ext.logging]` CHANGELOG
entry).

**Read first:** `cement/ext/ext_logging.py` lines 360-385.

---

### `cement/ext/ext_smtp.py:116-158` (send() docstring)

**Analog:** self, lines 140-143 (the `Returns:` block); the RST
`.. deprecated::` directive is a Sphinx built-in (no in-repo
precedent — first use). The runtime callsite at lines 189-191
(`# Deprecation: bool return will change to senderrs dict` +
`deprecate('3.0.16-1')`) **stays unchanged**; the docstring note is
a separate surface.

**Current state** (`cement/ext/ext_smtp.py:140-143`, focus on
Returns + Example boundary):

```python
        Returns:
            bool:``True`` if message is sent successfully, ``False`` otherwise

        Example:
```

**Target state** (D-04 — insert `.. deprecated::` admonition between
Returns and Example, per RESEARCH.md Example 4):

```python
        Returns:
            bool: ``True`` if message is sent successfully, ``False`` otherwise

        .. deprecated:: 3.0.16
            The ``bool`` return is deprecated and will change to the
            ``smtplib`` senderrs ``dict`` in Cement v3.2.0. See
            ``DEPRECATIONS['3.0.16-1']``.

        Example:
```

**Two changes:**
1. `bool:``True``` → `bool: ``True``` (insert one space — minor
   docstring rendering improvement; was a zero-space-after-colon RST
   formatting bug). Zero-risk.
2. Insert blank line + `.. deprecated::` directive + 3-line indented
   body + blank line, immediately before `Example:`. The directive
   renders as a "Deprecated since version 3.0.16" admonition in
   autodoc HTML.

**Why mechanical:** RST `.. deprecated::` is the canonical
Sphinx-built-in admonition for this purpose; no custom theme or
extension needed. Indentation MUST be 4 spaces (matches the rest of
the docstring body at 8-space indent for Args/Returns/Example
section labels and 12-space indent for body text — `.. directive::`
sits at body-text indent).

**Pitfall (per RESEARCH.md Pitfall 5):** This edit MUST land BEFORE
the `make docs -W` flag flip (commit 9). If the directive is
mis-indented, autodoc emits a warning and the `-W` gate breaks the
build the next time it runs.

**Read first:** `cement/ext/ext_smtp.py` lines 110-200 (covers the
`send()` method, the Returns block, the `Example:` block, and the
runtime callsite at line 189-191 — confirms the docstring edit
doesn't accidentally drift into the runtime code).

**Commit:** `refactor(ext.smtp): document send() bool-return removal
in v3.2.0` (D-16 step 3; CHANGELOG bucket: `Refactoring:` →
`[ext.smtp] Document send() bool-return removal in v3.2.0`).

---

### `cement/utils/shell.py:35-39` (cmd() docstring RST fix)

**Analog:** self, lines 35-39 (the offending docstring prose).
Sibling `exec_cmd()` docstring at lines 86-91 carries the **same**
prose pattern but is NOT in the live warning list — out of scope per
CONTEXT.md D-08 #4 (see RESEARCH.md Example 5 + Pitfall 9 reference).

**Current state** (`cement/utils/shell.py:35-39`):

```python
        tuple: When ``capture==True``, returns the ``(stdout, stderror,
            return_code)`` of the command. ``stdout`` and ``stderror`` are
            ``bytes`` (the ``Popen`` default); decode with the appropriate
            encoding if string output is needed, or pass ``text=True`` /
            ``encoding=...`` through ``**kwargs``.
```

**Target state** (D-08 #4 — single-token swap `/` → `or`):

```python
        tuple: When ``capture==True``, returns the ``(stdout, stderror,
            return_code)`` of the command. ``stdout`` and ``stderror`` are
            ``bytes`` (the ``Popen`` default); decode with the appropriate
            encoding if string output is needed, or pass ``text=True`` or
            ``encoding=...`` through ``**kwargs``.
```

**Why mechanical:** docutils trips on the slash between two adjacent
inline literals (`` ``text=True`` / ``encoding=...`` ``) — it reads
the run as a single ambiguous literal and fails to close. Replacing
the slash with `or` (or any non-symbol English word) gives docutils
breathing room. Per RESEARCH.md Pitfall 3, the alternative
(reformat into two sentences) is equally valid; the planner picks
the smaller diff.

**Pitfall (per RESEARCH.md Pitfall 3):** Do NOT add a stray backtick
or change the inline-literal counts; the warning is a parser
ambiguity, not a missing backtick. The fix is to **separate the two
literals with a non-backtick token**.

**Read first:** `cement/utils/shell.py` lines 1-66 (covers `cmd()`
+ `exec_cmd()` so the executor confirms `exec_cmd()` is intentionally
left alone).

**Commit:** `docs(utils.shell): fix inline-literal RST in cmd()
docstring` (D-16 step 8; CHANGELOG bucket: `Misc:` → `[docs] Fix
inline-literal RST in shell.cmd() docstring`).

---

### `cement/core/interface.py:102` (InterfaceManager.list — string-quote)

**Analog:** self, line 102 (the offending unquoted PEP 585 generic
on a method named `list`). Sibling pattern in
`cement/core/{hook,handler,extension}.py` uses `import builtins` +
`builtins.list[T]` — but **CONTEXT.md D-08 #3 explicitly picks
string-quote**, NOT the sibling pattern, to avoid an audit-public-api
baseline rebase. RESEARCH.md Open Question 1 confirms the choice.

**Current state** (`cement/core/interface.py:102`):

```python
    def list(self) -> list[str]:
```

**Target state** (D-08 #3 — string-quote + grep-able inline comment):

```python
    def list(self) -> "list[str]":  # autodoc: PEP 585 + method-name-shadow workaround
```

**Why this shape (not the sibling):**
- The method is named `list`, which **shadows the builtin** when
  autodoc's `inspect.signature()` introspects the method object —
  the unquoted `list[str]` annotation tries to subscript `self.list`
  (the method) instead of `builtins.list`.
- String-quoting defers annotation evaluation past method-name
  binding. Zero import added; zero audit-baseline change.
- The inline `# autodoc:` comment is grep-able (per CONTEXT.md
  Discretion item) so a future cleanup doesn't silently undo it.

**Pre-flight verification (per CONTEXT.md D-18 #3 + RESEARCH.md
Pitfall 1):**
```bash
make audit-public-api && echo OK_BEFORE
# apply the edit
make audit-public-api && echo OK_AFTER
```
**Pre-verified safe (RESEARCH.md Pitfall 1):** `audit-public-api.py`
walks AST names only; it never serializes annotations. The
string-quote does NOT change audit output. Run the check anyway as
hygiene, but treat it as **confirmation**, not a branch point.

**Read first:** `cement/core/interface.py` lines 90-120 (covers the
`get` method above and the `list` method + the `define` method
below — confirms scope is single-line + comment) AND
`scripts/audit-public-api.py` (skim to confirm RESEARCH.md
Pitfall 1's "annotation-blind" claim is accurate before committing).

**Commit:** `fix(core.interface): string-quote list[str] return
annotation for autodoc compatibility` (D-16 step 7; CHANGELOG
bucket: `Bugs:` → `[core.interface] String-quote list[str] return
annotation for autodoc compatibility`).

---

### `docs/source/conf.py` (duplicate html_theme_options dict)

**Analog:** self — lines 19-33 (the **kept** dict with the active
toc-config) vs lines 51-53 (the **deleted** duplicate that contains
only the unsupported `'logo'` key).

**Current state** (two competing assignments; the second silently
overwrites the first at module-load time):

```python
# lines 19-33 (active toc-config — KEEP):
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': True
}

# ... (commented-out alabaster/guzzle blocks, lines 35-50) ...

# lines 51-53 (DELETE — overwrites lines 19-33):
html_theme_options = {
    'logo': 'logo-text.png',
}
```

**Target state** (D-08 #1 — delete lines 51-53 entirely):

```python
# lines 19-33 unchanged (active toc-config — now the only assignment)

# ... (commented-out alabaster/guzzle blocks, lines 35-50, unchanged) ...

# (lines 51-53 deleted; line 54 onwards shifts up by 3 lines)
```

**Why this exact fix (per RESEARCH.md Pitfall 2 — CRITICAL):**
- Naive fix "remove the `'logo'` key" → empty dict
  `html_theme_options = {}` → second-assignment-wins still clobbers
  lines 19-33 → navigation rendering silently degrades. The
  `'logo'` warning DOES go away, but the bug shifts.
- Correct fix: delete the **entire second assignment** (3 lines, all
  of `html_theme_options = {` / `'logo': '...'` / `}`). Lines 19-33
  then become the live config.

**Pitfall (per RESEARCH.md Pitfall 2):** Task wording MUST say
"delete lines 51-53 in `docs/source/conf.py` (the duplicate
`html_theme_options` assignment)". NOT "remove the 'logo' key".
The verification step should check **both** that the warning is
gone AND that `navigation_depth: 4` (or any other toc-config key) is
still present in the only remaining `html_theme_options` dict.

**Read first:** `docs/source/conf.py` lines 14-55 (covers BOTH the
line-19 and line-51 dicts so the executor sees the duplication
firsthand and doesn't apply the naive fix).

**Commit:** `docs(sphinx): drop unsupported 'logo' theme option from
conf.py` (D-16 step 5; CHANGELOG bucket: `Misc:` → `[docs] Drop
unsupported 'logo' theme option from sphinx conf`).

---

### `docs/source/index.rst` and/or `docs/source/api/index.rst` (toctree wiring)

**Analog:** self — `docs/source/index.rst` lines 8-13 is the live
top-level toctree that already references the three child indexes;
`docs/source/api/index.rst` is the orphan duplicate.

**Current state — `docs/source/index.rst:1-13`** (the kept file):

```rst
API Reference
==============================================================================

.. note:: This documentation is strictly for API reference.  For more complete
   developer documentation, please visit the official site
   http://builtoncement.com.

.. toctree::
   :maxdepth: 2

   api/core/index
   api/utils/index
   api/ext/index
```

**Current state — `docs/source/api/index.rst:1-14`** (the orphan):

```rst

API Reference
==============================================================================

.. note:: This documentation is strictly for API reference.  For more complete
   developer documentation, please visit the official site
   http://builtoncement.com.

  .. toctree::
     :maxdepth: 1

     core/index
     utils/index
     ext/index
```

**Target state — option (a), RECOMMENDED per RESEARCH.md Pitfall 4:**

Delete `docs/source/api/index.rst` entirely. The top-level
`docs/source/index.rst` already references `api/core/index`,
`api/utils/index`, `api/ext/index` — no further edits needed.

**Target state — option (b), fallback if external links land on
`api/index.html`:**

Add a `:hidden:` toctree to `docs/source/index.rst`:
```rst
.. toctree::
   :hidden:

   api/index
```
This absorbs the orphan into the document graph without surfacing
it twice in the rendered nav.

**Pre-flight check (RESEARCH.md Pitfall 4):**
```bash
grep -rn 'api/index' .planning/ docs/ README.md
```
If the only references are inside `docs/source/` itself, option (a)
is safe. Otherwise, default to option (b).

**Read first:** `docs/source/index.rst` (14 lines) AND
`docs/source/api/index.rst` (14 lines) — both files are tiny.

**Commit:** `docs(sphinx): wire api/index into top-level toctree`
(D-16 step 6; CHANGELOG bucket: `Misc:` → `[docs] Wire api/index
into top-level toctree`).

---

### `Makefile` (docs target — wire -W + AUDIT POINT)

**Analog:** self — current lines 62-66 (the `docs:` target). The
**AUDIT POINT comment shape** mirrors the existing AUDIT POINT
comments in `pyproject.toml` (Phase 1 D-08 + Phase 2 D-12 + D-10/D-11
+ Phase 3 D-06 precedent).

**Current state** (`Makefile:62-66`):

```makefile
docs:
	cd docs; pdm run sphinx-build ./source ./build; cd ..
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo
```

**Existing in-repo AUDIT POINT precedent** (`pyproject.toml:79-82`):

```toml
[tool.coverage.report]
# AUDIT POINT (Phase 2 D-10/D-11): fail_under = 100 is the absolute
# coverage gate. Belt-and-braces: pytest addopts also passes
# --cov-fail-under=100 in case future pytest-cov bumps change
# pyproject discovery semantics.
precision = 2
fail_under = 100
```

**Target state** (D-08 #5 / D-09 — flag + AUDIT POINT mirroring the
pyproject pattern):

```makefile
docs:
	# AUDIT POINT (Phase 5 D-09): -W enforces zero docs warnings.
	# If a future warning is acceptable, suppress it explicitly via
	# conf.py suppress_warnings rather than reverting -W. Mirrors
	# Phase 1 D-08 / Phase 2 D-10/D-11 (no implicit drift).
	cd docs; pdm run sphinx-build -W ./source ./build; cd ..
	@echo
	@echo DOC: "file://"$$(echo `pwd`/docs/build/html/index.html)
	@echo
```

**Why this exact shape:**
- `-W` flag inserted between `sphinx-build` and `./source` (matches
  sphinx CLI grammar: `sphinx-build [OPTIONS] SOURCE BUILD`).
- AUDIT POINT comment is `#` (Make's comment char inside a recipe
  is `#`; tabs precede each line so Make includes them in the recipe
  but they're no-op shell comments at run-time).
- The `(Phase 5 D-09)` parenthetical follows the established convention
  in `pyproject.toml` (`(Phase 2 D-12)`, `(Phase 2 D-10/D-11)`,
  `(D-08, Phase 03 D-06)`, etc.).

**Pitfall (per RESEARCH.md Pitfall 5):** This commit (D-16 step 9)
MUST land AFTER all 4 sphinx fixes (steps 5-8). If the planner
reorders, the `-W` flag goes live while a docstring warning is still
emitting and `make docs` breaks for the rest of the phase.

**Read first:** `Makefile` (94 lines, whole file — confirm only the
`docs:` recipe is touched) AND `pyproject.toml` lines 60-105
(confirm AUDIT POINT comment style — multi-line `# AUDIT POINT
(<phase ref>): <rationale>` with the rationale wrapped at 78 chars).

**Commit:** `chore(make): wire -W into make docs (zero-warnings
gate)` (D-16 step 9; CHANGELOG bucket: `Misc:` → `[dev] Wire -W into
make docs (zero-warnings gate)`).

---

### `README.md` (drop Travis CI surfaces)

**Analog:** self — current line 5 (the badge) + line 60 (the
list-item link). Both surfaces are the only `travis-ci` references in
the file.

**Current state — line 5** (the badge):

```markdown
[![Continuous Integration Status](https://app.travis-ci.com/datafolklabs/cement.svg?branch=master)](https://app.travis-ci.com/github/datafolklabs/cement/)
```

**Current state — line 60** (the list-item link):

```markdown
- [Travis CI](https://travis-ci.org/datafolklabs/cement/)
```

**Target state** (D-10 — delete both lines):

- Line 5: deleted (the surrounding lines 3, 4, 6 all stay; the badge
  block becomes 2 badges instead of 3).
- Line 60: deleted (the surrounding list items at lines 57-61 stay;
  the list shrinks from 5 items to 4).

**Why mechanical:** Two single-line deletions in a markdown file. No
other edits to README.md in this phase (D-10 explicitly forbids
walkthrough-driven additions / Cement 4 forward-signaling).

**Acceptance grep** (D-18 #8):
```bash
grep -E 'travis-ci' README.md | wc -l
# expected: 0
```

**Read first:** `README.md` lines 1-65 (covers the badge block,
"More Information" list, and confirms no other Travis references
live elsewhere in the file).

**Commit:** `docs(readme): drop Travis CI link (moved to GitHub
Actions)` (D-16 step 10; CHANGELOG bucket: `Misc:` → `[docs] Drop
Travis CI link/badge (CI moved to GitHub Actions)`).

---

### `.github/CONTRIBUTING.md` (Conventional Commits alignment)

**Analog:** self — current lines 33-80 (the existing "Guidelines for
Code Contributions" section). The replacement section anchors on
`CLAUDE.md` §"Commit Conventions" as the canonical commit-shape doc.

**Current state — line 55** (the load-bearing line to replace):

```markdown
- A single commit per issue.
```

**Plus surrounding context lines 33-80** that need partial refresh
(see RESEARCH.md Example 9 for the full replacement section).

**Target state** (D-10 — full section replacement per RESEARCH.md
Example 9):

```markdown
## Guidelines for Code Contributions

All contributors should attempt to abide by the following:

- Contributors fork the project on GitHub onto their own account
- All changes should be committed and pushed to their repository
- All pull requests are from a topic branch, not an existing Cement
  branch
- Contributors make every effort to comply with [PEP8]
- Before starting on a new feature or bug fix, do the following:
    - `git pull --rebase` to get latest changes from upstream
    - Checkout a new branch. For example:
        - `git checkout -b feature/slug-name`
        - `git checkout -b bug/github-issue-number`
- Code must include the following:
    - All tests pass successfully (`make test`)
    - Coverage reports 100% code coverage (`make test`)
    - Compliance passes (`make comply` — runs `ruff` and `mypy`)
    - New features are documented in the appropriate API docstring
    - User-visible changes are recorded in `CHANGELOG.md` under the
      active development section, in one of the standard buckets
      (`Bugs`, `Features`, `Refactoring`, `Misc`, `Deprecations`)
- All contributions should be associated with at least one issue in
  GitHub. If the issue does not exist, create one (per the
  guidelines above).
- Contributors should add their full name or handle to the
  `CONTRIBUTORS` file.

### Commit Conventions

Cement follows [Conventional Commits] for all commit messages.
Commits are atomic per concern — one logical change per commit, not
"a single commit per issue" (which often lumps unrelated edits).

- **Subject line:** `<type>(<area>): <imperative summary>`
  (max 78 chars)
- **Type:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`
- **Body:** wrap at 78 chars; explain the *why*, not just the *what*
- **Authoring:** Run `make commit` to use the project's
  `commitizen` (`cz`) interactive prompt. It enforces the format and
  the wrap.

See [`CLAUDE.md`](../CLAUDE.md) §"Commit Conventions" for the
canonical commit-shape doc.

[Conventional Commits]: https://www.conventionalcommits.org/
```

**Why this exact shape (per RESEARCH.md Example 9):**
- Drops "A single commit per issue" (line 55 — the load-bearing
  conflict with current project discipline).
- Adds a new `### Commit Conventions` subsection that codifies
  Conventional Commits + 78-char wrap + `make commit`.
- Anchors on `CLAUDE.md` §"Commit Conventions" (back-relative
  link `../CLAUDE.md` since CONTRIBUTING.md lives in `.github/`).
- Preserves the existing `[Open Source Initiative]`, `[issue tracker]`,
  `[PEP8]`, `[Commit Guidelines]` reference-link block at the bottom
  of the file (lines 82-85) — adds `[Conventional Commits]:
  https://www.conventionalcommits.org/` as a sibling link.

**Acceptance grep** (D-18 #9):
```bash
grep -cE 'Conventional Commits' .github/CONTRIBUTING.md
# expected: ≥1
grep -c 'make commit' .github/CONTRIBUTING.md
# expected: ≥1
```

**Read first:** `.github/CONTRIBUTING.md` (whole file, 86 lines) AND
`CLAUDE.md` §"Commit Conventions" (the canonical commit-shape doc
that the replacement section anchors on).

**Commit:** `docs(contributing): align with Conventional Commits +
atomic-per-concern discipline` (D-16 step 11; CHANGELOG bucket:
`Misc:` → `[docs] Align CONTRIBUTING with Conventional Commits +
atomic-per-concern`).

---

### `DEPRECATIONS.md` (NEW, repo root — per-deprecation H2 blocks)

**Analog:** sibling repo-root markdown shape — `CHANGELOG.md` (H2
sections, no frontmatter) and `CONTRIBUTORS.md` (no frontmatter,
plain repo-root markdown). The **per-deprecation block structure**
itself has no in-repo precedent; D-07 establishes the convention.

**Sibling shape — `CHANGELOG.md:1-3`** (no-frontmatter, H1+H2):

```markdown
# ChangeLog

## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)
```

**Sibling shape — `CONTRIBUTORS.md:1-4`** (no-frontmatter, H1 +
prose):

```markdown
# Contributors

The following people have contributed to Cement, either by way of source code,
documentation, or testing:
```

**Target state — `DEPRECATIONS.md`** (D-06/D-07; full template per
RESEARCH.md Example 8):

```markdown
# Cement Deprecations

This document mirrors the canonical GitBook narrative at
[docs.builtoncement.com/release-information/deprecations](https://docs.builtoncement.com/release-information/deprecations)
for in-repo discoverability. Each deprecation has an H2 section with
its registry ID. New IDs append at the bottom under their
since-version section.

For runtime behavior, the `cement.core.deprecations.deprecate()`
helper emits a `DeprecationWarning` whose message includes a
back-link to the corresponding GitBook anchor.

## 3.0.8-1

**Surface:** Environment variable `CEMENT_FRAMEWORK_LOGGING`
**Since:** Cement 3.0.8
**Removal:** Cement v3.2.0

Use `CEMENT_LOG` instead. Single-pass migration:

```bash
# Before
export CEMENT_FRAMEWORK_LOGGING=true

# After
export CEMENT_LOG=true
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.8-1)

## 3.0.8-2

**Surface:** `App.Meta.framework_logging`
**Since:** Cement 3.0.8
**Removal:** Cement v3.2.0

Will be changed or removed. Migrate to the `CEMENT_LOG` environment
variable surface (see `3.0.8-1`).

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.8-2)

## 3.0.10-1

**Surface:** `cement.ext.ext_logging.LoggingLogHandler.fatal()` /
`set_level('FATAL')`
**Since:** Cement 3.0.10
**Removal:** Cement v3.2.0

Use `critical()` / `set_level('CRITICAL')` instead.

```python
# Before
app.log.fatal('something broke')
app.log.set_level('FATAL')

# After
app.log.critical('something broke')
app.log.set_level('CRITICAL')
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.10-1)

## 3.0.16-1

**Surface:** `cement.ext.ext_smtp.SMTPMailHandler.send()` return type
**Since:** Cement 3.0.16
**Removal:** Cement v3.2.0

The `bool` return value is deprecated; in v3.2.0 the method will
return the `smtplib` senderrs `dict`.

```python
# Before (3.0.x)
ok = app.mail.send('hello')
if not ok:
    handle_error()

# After (3.2.0+)
errs = app.mail.send('hello')
if errs:
    handle_error_per_recipient(errs)
```

[GitBook reference](https://docs.builtoncement.com/release-information/deprecations#3.0.16-1)
```

**Why this exact structure (per CONTEXT.md D-07 + RESEARCH.md
Example 8):**
- One H2 section per deprecation ID, ordered by since-version
  ascending (so new IDs append at the bottom under their
  since-version section without re-grouping).
- Each section carries the locked five-element layout: `**Surface:**`,
  `**Since:**`, `**Removal:**`, migration prose with code example,
  `[GitBook reference]` back-link.
- **GitBook anchor format is dotted** (`#3.0.8-1`, NOT `#3-0-8-1`)
  per `cement/core/deprecations.py:15` `deprecate()` URL convention.
  See RESEARCH.md Pitfall 8.

**Pitfall (per RESEARCH.md Pitfall 8):** Anchor format MUST be
`#<major>.<minor>.<patch>-<n>` literally (dotted, with hyphen before
the disambiguator). Do NOT GitHub-slugify to `#3-0-8-1`.

**Acceptance grep** (D-18 #7):
```bash
test -f DEPRECATIONS.md && grep -cE '^## 3\.0\.' DEPRECATIONS.md
# expected: 4
grep -E 'docs.builtoncement.com/release-information/deprecations#3\.0\.' DEPRECATIONS.md | wc -l
# expected: ≥4 (one back-link per ID)
```

**Read first:** `cement/core/deprecations.py` (DEPRECATIONS dict —
the 4 IDs source-of-truth) AND `CHANGELOG.md` lines 1-5 (sibling
H2 shape — confirms the no-frontmatter convention).

**Commit:** `docs: add top-level DEPRECATIONS.md` (D-16 step 4;
CHANGELOG bucket: `Misc:` → `[docs] Add top-level DEPRECATIONS.md
mirroring GitBook narrative`. Could also be `Features:` if planner
prefers — D-16 calls this judgment, leans Misc per RESEARCH.md
Pitfall 7 table).

---

### `.planning/codebase/CONVENTIONS.md` (PEP 604/585 closeout)

**Analog:** self — current line 35 (the **only** stale surface; body
of "Type annotations" section at lines 22-26 and 92-95 is **already**
in PEP 604/585 form per RESEARCH.md Pitfall 6 / Assumption A6).

**Current state — line 35** (the only stale surface):

```
target-version = "py39"
```

(Inside the `**Ruff Configuration**` code block at lines 37-45.)

**Live `pyproject.toml:88`** (the source of truth — already updated
in Phase 1):

```toml
target-version = "py310"
```

**Target state** (D-12 — sync the example to the live config):

```
target-version = "py310"
```

**Why this exact change (per RESEARCH.md Pitfall 6 — CRITICAL):**
- The "deferred CONVENTIONS refresh" framing in CONTEXT.md D-12
  implies a wholesale rewrite. **Reality: the rewrite is already
  done** — Phase 3 Plan 03 UP cascade landed the body changes.
- The single residual stale surface is line 35's `py39` inside the
  illustrative ruff config block. Update to `py310` to match the
  live `pyproject.toml:88`.
- **NOT a wholesale rewrite.** The plan task should specify a
  pre-task grep:
  ```bash
  grep -nE 'Dict\[|List\[|Optional\[|Union\[|target-version' \
       .planning/codebase/CONVENTIONS.md
  ```
  Expected: only line 35 hits. If body-text `Dict/List/Optional/Union`
  hits surface, the doc was reverted — escalate to wholesale refresh.

**Pitfall (per RESEARCH.md Pitfall 6):** Plan task description MUST
NOT estimate "rewrite the entire Type annotations paragraph". The
commit subject can stay generic (`docs(codebase): refresh
CONVENTIONS to PEP 604/585 syntax`) since it captures the *intent*,
but the diff is 1 line, not a section rewrite.

**Read first:** `.planning/codebase/CONVENTIONS.md` lines 22-100
(covers the Type annotations section at 22-26, the Ruff Configuration
example at 37-45 with the line-35 target, and the sister Type
Annotations section at 83-100 — confirms 92-95 is also already in
modern form).

**Commit:** `docs(codebase): refresh CONVENTIONS to PEP 604/585
syntax` (D-16 step 13; CHANGELOG: **NO ENTRY** — this is a
`.planning/` planning-artifact edit per CLAUDE.md §"Changelog
Maintenance" filter rule. See "Shared Patterns / CHANGELOG bucket
mapping" below.).

---

### `.planning/REQUIREMENTS.md` (SECv2-01..03 expansion)

**Analog:** self — current lines 89-94 (the existing one-liner
`SECv2-01..04` block). **Anchor pattern** for the multi-line shape
mirrors the `### Release` `REL-01..05` block elsewhere in the doc
(multi-line entries with sub-bullets) and the live Phase 2 capture
artifact `02-PIP-AUDIT.md` (which RESEARCH.md identifies as the
SECv2-01 anchor).

**Current state** (`.planning/REQUIREMENTS.md:89-94`):

```markdown
### Security Audit Tooling Implementation

- **SECv2-01**: `pip-audit` integrated into CI on every PR
- **SECv2-02**: `bandit` integrated into CI on every PR with project-tuned ruleset
- **SECv2-03**: SAST tool (CodeQL or Semgrep) selected and integrated into CI
- **SECv2-04**: Documented security disclosure process (`SECURITY.md`)
```

**Target state** (D-13/D-14 — expand first three; SECv2-04 unchanged
per D-13; full text per RESEARCH.md Example 10):

```markdown
### Security Audit Tooling Implementation

- **SECv2-01**: `pip-audit` integrated into CI on every PR
    - **Tool:** `pdm run pip-audit` (read deps from `pdm.lock`)
    - **Make target:** `make audit-deps` — independent target, NOT
      chained into `make test` or `make comply` (matches Phase 03
      D-03 `audit-public-api` discipline)
    - **CI placement:** new dedicated workflow file
      `.github/workflows/security.yml`, triggers on `pull_request`
      + weekly `cron`. NOT serialized into `build_and_test.yml`
      (mirrors Phase 02 D-16 fail-fast vs feedback-time tradeoff)
    - **Config:** none initially; `pip-audit --skip` for accepted
      CVEs documented inline if any surface
    - **New dev-dep:** `pip-audit` (PyPI; latest stable)
    - **Exit behavior:** advisory on first run (Phase 02 D-03
      one-shot precedent — capture accepted CVEs in an in-repo
      artifact mirroring `02-PIP-AUDIT.md`); flip to blocking once
      baseline is clean
    - **Anchor:** `.planning/phases/02-dependencies-ci-pipeline/02-CONTEXT.md`
      D-03 + `02-PIP-AUDIT.md` capture artifact

- **SECv2-02**: `bandit` integrated into CI on every PR with project-tuned ruleset
    - **Tool:** `pdm run bandit -r cement/`
    - **Make target:** `make audit-bandit` — independent target
    - **CI placement:** same `.github/workflows/security.yml` lane
      as SECv2-01 (one workflow, three jobs)
    - **Config:** `.bandit` allowlist file at repo root —
      project-tuned to skip false positives on framework-intentional
      patterns (e.g., `subprocess` call sites in `cement/utils/shell.py`
      that are deliberate per the public API contract)
    - **New dev-dep:** `bandit` (PyPI; latest stable)
    - **Exit behavior:** advisory on first run; flip to blocking
      once `.bandit` allowlist is curated
    - **Anchor:** `02-CONTEXT.md` D-03 (same one-shot precedent)

- **SECv2-03**: SAST tool (CodeQL or Semgrep) selected and integrated into CI
    - **Tool:** TBD per evaluation; candidates are CodeQL (GitHub-
      native, free for public repos, deeper Python rules) and
      Semgrep (rule customization, more permissive licensing)
    - **Make target:** `make audit-sast` (only if CLI-runnable;
      CodeQL is GitHub-Actions-only)
    - **CI placement:** dedicated job in `security.yml`; weekly
      cron preferred over per-PR (run-time cost)
    - **Config:** `.semgrep.yml` (Semgrep) OR
      `.github/codeql/codeql-config.yml` (CodeQL) — rule selection
      pinned to Python OWASP top-N + cement-specific patterns
    - **New dev-dep:** `semgrep` if Semgrep selected; none if
      CodeQL (GitHub-hosted)
    - **Exit behavior:** advisory on first run; per-finding triage
      before any blocking flip
    - **Anchor:** `02-CONTEXT.md` D-03

- **SECv2-04**: Documented security disclosure process (`SECURITY.md`)
```

**Why this exact shape (per CONTEXT.md D-14):**
- Six locked sub-bullets per stub: `**Tool:**`, `**Make target:**`,
  `**CI placement:**`, `**Config:**`, `**New dev-dep:**`,
  `**Exit behavior:**`. (`**Anchor:**` is a seventh sub-bullet but
  optional — present for SECv2-01..03 to point at the Phase 02 D-03
  precedent.)
- 4-space indent for sub-bullets (markdown list nesting).
- SECv2-04 line stays as-is — it's a distinct concern (disclosure
  process, not tooling) per D-13.

**Acceptance grep** (D-18 #12):
```bash
awk '/SECv2-01/,/SECv2-04/' .planning/REQUIREMENTS.md | \
    grep -cE '\*\*Tool:\*\*|\*\*Make target:\*\*|\*\*CI placement:\*\*|\*\*Config:\*\*|\*\*New dev-dep:\*\*|\*\*Exit behavior:\*\*'
# expected: ≥18 (6 properties × 3 stubs)
```

**Read first:** `.planning/REQUIREMENTS.md` lines 70-100 (covers the
v1 `SEC-01..03` one-liners at 73-75, the v2 `SECv2-01..04` block at
89-94 to be expanded, and the surrounding `### Release` /
`### Performance Pass` blocks for nearby format precedent) AND
`.planning/phases/02-dependencies-ci-pipeline/02-PIP-AUDIT.md`
(skim to confirm it's the right "capture artifact" pattern that the
SECv2-01 stub references).

**Commit:** `docs(05): expand SECv2-01..03 with phase-shaped scope
notes` (D-16 step 14; CHANGELOG: **NO ENTRY** — `.planning/` edit,
filtered per CLAUDE.md §"Changelog Maintenance").

---

### `CHANGELOG.md` (per-commit append, NOT a section cut)

**Analog:** self — `## 3.0.15 - DEVELOPMENT` section already populated
with 100+ existing entries across 5 buckets. Phase 5 appends; it does
NOT cut a new section header (that's Phase 6 / DOCS-03).

**Existing bucket headers in the active section** (`CHANGELOG.md`
lines 3-322; verified via grep):

```
## 3.0.15 - DEVELOPMENT (will be released as stable/3.0.16)   # line 3

Bugs:                                                          # line 5
Features:                                                      # line 138
Refactoring:                                                   # line 142
Misc:                                                          # line 293
Deprecations:                                                  # line 322
```

**Existing entry shape** (sample from line 7, `Bugs:` bucket):

```markdown
- `[ext.smtp]` Fix `timeout` passed as `local_hostname` in SMTP constructors
```

Wider entries wrap at 78 chars (verified — e.g., `[ext.smtp]` block
at lines 35-52 wraps).

**Target state:** Append 11 entries across the 5 buckets (per the
bucket-mapping table in RESEARCH.md Pitfall 7 — reproduced under
"Shared Patterns / CHANGELOG bucket mapping" below). Do NOT add
entries for commits 13 and 14 (they edit `.planning/` only, which
CLAUDE.md §"Changelog Maintenance" filters out).

**Why mechanical:** Each Phase 5 source/doc commit lands one CHANGELOG
line in its corresponding bucket as part of the commit. The shape is
`- ` `[<area>]` ` <imperative-summary>`. 78-char wrap if the line
exceeds the limit.

**Read first:** `CHANGELOG.md` lines 1-325 (covers the active section
header + all 5 bucket headers + a sample of existing entries from
each bucket so the executor matches shape exactly).

**Commit:** Each Phase 5 commit (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
includes its CHANGELOG.md append in the same commit — NOT separately
committed. Phase 5 D-16 is explicit about this; CLAUDE.md is the
authority.

---

## Shared Patterns

### Atomic-per-concern Conventional Commits (carries Phase 1/2/3)

**Source:** `CLAUDE.md` §"Commit Conventions" (canonical) +
`.planning/phases/01-tooling-baseline-python-matrix/01-CONTEXT.md`
D-02/D-04 + `.planning/phases/03-internal-refactor-coverage-hardening/03-CONTEXT.md`
D-22 (precedent commit sequences).

**Apply to:** All 14 Phase 5 commits.

**Shape:**
```
<type>(<area>): <imperative-summary, ≤78 chars>

<body, wrapped at 78 chars; explain the *why*, not just the *what*>
```

**Type → CHANGELOG bucket mapping** (per CLAUDE.md §"Changelog
Maintenance" + RESEARCH.md Pitfall 7):

| Conventional type | CHANGELOG bucket | Notes |
|-------------------|------------------|-------|
| `fix:` | `Bugs:` | Used for `interface.py:102` autodoc workaround |
| `feat:` | `Features:` | Not used in Phase 5 |
| `refactor:` | `Refactoring:` | Used for `core.deprecations` registry pin + `ext.logging` / `ext.smtp` docstring sweeps |
| `docs:` | `Misc:` (judgment call; new files may pick `Features:`) | Used for sphinx fixes, README, CONTRIBUTING, DEPRECATIONS.md |
| `chore:` | `Misc:` | Used for `Makefile docs:` `-W` flag (`[dev]` area tag) |
| `test:` | `Misc:` (or skip) | Not used in Phase 5 |
| `ci:` | `Misc:` (`[ci]` area tag) | Not used in Phase 5 |

**Example body** (per RESEARCH.md Pattern 1 / commit 1):

```
refactor(core.deprecations): tighten removal-version language

Pin 3.0.10-1 (FATAL logging) and 3.0.16-1 (SMTPMailHandler.send bool
return) to v3.2.0 in DEPRECATIONS dict. Aligns with the existing
3.0.8-1 / 3.0.8-2 policy. Removal target is the next breakage-allowed
minor; downstream apps that have ignored the warning since 3.0.10
have had ample time.

DEPREC-01 acceptance criterion #5: every entry in
cement/core/deprecations.py:DEPRECATIONS now names a removal version.
DEPREC-03 already-satisfied — existing tests assert by ID, not by
message text.
```

---

### CHANGELOG bucket mapping (per Phase 5 commit)

**Source:** RESEARCH.md Pitfall 7 + CLAUDE.md §"Changelog Maintenance"
(filter rule for planning-artifact commits).

**Apply to:** Each of the 14 commits in D-16. The planner MUST
encode this table in the per-task acceptance criteria so the executor
doesn't blindly add 14 entries (only 11 land).

| # | Commit subject | Bucket | CHANGELOG entry text |
|---|----------------|--------|----------------------|
| 1 | `refactor(core.deprecations): tighten removal-version language` | `Refactoring:` | `[core.deprecations] Pin 3.0.10-1 and 3.0.16-1 removal version to v3.2.0` |
| 2 | `refactor(ext.logging): tighten FATAL deprecation removal version in docstrings` | `Refactoring:` | `[ext.logging] Tighten FATAL deprecation removal version in docstrings` |
| 3 | `refactor(ext.smtp): document send() bool-return removal in v3.2.0` | `Refactoring:` | `[ext.smtp] Document send() bool-return removal in v3.2.0` |
| 4 | `docs: add top-level DEPRECATIONS.md` | `Misc:` | `[docs] Add top-level DEPRECATIONS.md mirroring GitBook narrative` |
| 5 | `docs(sphinx): drop unsupported 'logo' theme option from conf.py` | `Misc:` | `[docs] Drop unsupported 'logo' theme option from sphinx conf` |
| 6 | `docs(sphinx): wire api/index into top-level toctree` | `Misc:` | `[docs] Wire api/index into top-level toctree` |
| 7 | `fix(core.interface): string-quote list[str] return annotation for autodoc compatibility` | `Bugs:` | `[core.interface] String-quote list[str] return annotation for autodoc compatibility` |
| 8 | `docs(utils.shell): fix inline-literal RST in cmd() docstring` | `Misc:` | `[docs] Fix inline-literal RST in shell.cmd() docstring` |
| 9 | `chore(make): wire -W into make docs (zero-warnings gate)` | `Misc:` | `[dev] Wire -W into make docs (zero-warnings gate)` |
| 10 | `docs(readme): drop Travis CI link (moved to GitHub Actions)` | `Misc:` | `[docs] Drop Travis CI link/badge (CI moved to GitHub Actions)` |
| 11 | `docs(contributing): align with Conventional Commits + atomic-per-concern discipline` | `Misc:` | `[docs] Align CONTRIBUTING with Conventional Commits + atomic-per-concern` |
| 12 | `docs(<area>): drop stale <thing> reference` | (n/a) | **0 commits** — pre-verified 0 docstring hits per RESEARCH.md Assumption A5. |
| 13 | `docs(codebase): refresh CONVENTIONS to PEP 604/585 syntax` | **NO ENTRY** | `.planning/` edit — planning-artifact, filtered per CLAUDE.md §"Changelog Maintenance". |
| 14 | `docs(05): expand SECv2-01..03 with phase-shaped scope notes` | **NO ENTRY** | `.planning/REQUIREMENTS.md` edit — planning-artifact, filtered. The `docs(05): ...` subject prefix is itself the GSD planning-artifact convention (Phase 1/01.1/Phase 2/Phase 3 precedent). |

**Subtle point (per RESEARCH.md Pitfall 7):** Commits 13 and 14 are
`docs:` Conventional, but they edit `.planning/` files, which
CLAUDE.md filters out as "planning-artifact commits". The bucket is
**no entry**, NOT `Misc:`. This MUST be explicit in the plan.

**Acceptance grep** (after all 11 commits land):
```bash
# Count NEW entries appended in Phase 5 (compare against Phase 4 baseline)
git log --since=<phase-5-start> --pretty=format: --name-only | \
    grep CHANGELOG.md | wc -l
# expected: 11 (matches the 11 source/doc commits; 13 and 14 do NOT touch CHANGELOG)
```

---

### Hybrid AUDIT POINT inline comment (carries Phase 1 D-08 / Phase 2 D-12 / Phase 3 D-06)

**Source:** `pyproject.toml:68-71, 79-82, 102-110, 125, 145, 180`
(the existing AUDIT POINT comments in the live repo).

**Apply to:** `Makefile docs:` target only (D-09).

**Shape (multi-line `#` comment + recipe line):**

```makefile
docs:
	# AUDIT POINT (Phase 5 D-09): -W enforces zero docs warnings.
	# If a future warning is acceptable, suppress it explicitly via
	# conf.py suppress_warnings rather than reverting -W. Mirrors
	# Phase 1 D-08 / Phase 2 D-10/D-11 (no implicit drift).
	cd docs; pdm run sphinx-build -W ./source ./build; cd ..
```

**Rationale:**
- Grep-able: `grep -nE 'AUDIT POINT' Makefile pyproject.toml` finds
  every deliberate-configuration site across the repo.
- Phase reference parenthetical: `(Phase 5 D-09)` matches the
  established convention in `pyproject.toml`. Future cleanup PRs can
  trace the rationale without re-reading the phase artifacts.
- Wrapped at ~70 chars to fit within Makefile recipe indentation
  (recipe lines are tab-prefixed, so the effective wrap target is
  78 chars minus tab width).

---

### "In-place ratification of already-satisfied requirements" (Phase 4 precedent)

**Source:** `.planning/phases/04-backlog-triage/04-NOTE.md` (manual
pass; mark closed with note rather than synthetic work).

**Apply to:** DEPREC-03 in Phase 5 (per CONTEXT.md `<domain>` "no new
test cases needed; existing assertions test by ID, not by message
text"). The phase artifacts (PLAN.md tasks for DEPREC-03) reference
this precedent and explicitly note "no work — already satisfied by
`tests/core/test_deprecations.py` + `tests/ext/test_ext_smtp.py:631`".

**Shape (in PLAN.md task action text):**

```markdown
**DEPREC-03 acceptance:** already-satisfied. Per CONTEXT.md D-02 and
RESEARCH.md verification, all 4 deprecation IDs are asserted in the
existing test suite (3 in `tests/core/test_deprecations.py`, 1 in
`tests/ext/test_ext_smtp.py:631`). No new test work this phase.
Acceptance is verified by re-running `make test` and confirming the
4 assertions still pass — NOT by adding new test cases.
```

---

### REQUIREMENTS.md re-interpretation (established here in Phase 5 D-05)

**Source:** Phase 5 CONTEXT.md D-05 (first use; not a prior-phase
precedent). The pattern: when REQUIREMENTS.md wording was authored
without context that emerged later (e.g., DEPREC-02's "dedicated
`docs/source/deprecations.rst` page" was authored before the
"sphinx is API-only" docs-split was locked into `docs/source/index.rst`
line 4-6), surface the conflict in CONTEXT.md `<domain>`, document
the reinterpretation in `<decisions>`, write the in-repo artifact in
the correct shape (D-06: `DEPRECATIONS.md` not
`docs/source/deprecations.rst`).

**Apply to:** D-05/D-06 reinterpretation of DEPREC-02. Plan task for
commit 4 (`docs: add top-level DEPRECATIONS.md`) MUST cite this
reinterpretation in the rationale so a future reader of the
acceptance evidence understands why the artifact is at repo root,
not in `docs/source/`.

---

### Coverage hold-the-line (Phase 2 D-10/D-11)

**Source:** `pyproject.toml:78-84` `[tool.coverage.report]
fail_under = 100` + `[tool.pytest.ini_options] addopts =
"--cov-fail-under=100"` (belt-and-braces).

**Apply to:** Every Phase 5 commit. `make test` must exit 0 with
100% coverage on every commit. Phase 5 is doc-only, so:
- Commits 1, 2, 3, 7 (source-code edits in `cement/`) need full
  `make test` re-run as the per-commit gate.
- Commits 4, 5, 6, 8, 9, 10, 11, 13, 14 (no `cement/` source change)
  technically can't drop coverage, but `make test` is still cheap
  and `make comply` is mandatory regardless.

**Shape (in PLAN.md task action text):**

```markdown
**Per-commit gate:** Run `make comply && make test` before staging.
Both MUST exit 0. Commit if green; do NOT bypass with `--no-verify`.
```

---

## No Analog Found

| File | Role | Reason |
|------|------|--------|
| `DEPRECATIONS.md` per-block structure (5 fields per H2 section) | new repo-root markdown convention | No prior in-repo per-deprecation reference document exists. The repo-root markdown shape (no frontmatter, H1+H2) IS captured in the sibling `CHANGELOG.md` / `CONTRIBUTORS.md` analog above; the per-block field layout (`**Surface:**`, `**Since:**`, `**Removal:**`, code block, `[GitBook reference]`) is **established here** by D-07. The planner should treat the RESEARCH.md Example 8 template as the authoritative shape for this phase and any future deprecation appended after it. |
| `cement/ext/ext_smtp.py:send()` `.. deprecated::` RST admonition | RST autodoc directive insertion | No prior `.. deprecated::` directive exists in `cement/`'s docstring corpus. The directive is a Sphinx built-in; no custom theme/extension needed. The 4-space indent for the directive body is canonical Sphinx (matches `Args:`/`Returns:`/`Example:` body indentation). |

---

## Metadata

**Analog search scope:**
- `cement/core/{deprecations,interface,foundation,hook,handler,extension}.py`
  (registry + autodoc workaround precedent)
- `cement/ext/{ext_logging,ext_smtp}.py` (deprecation docstring sites)
- `cement/utils/shell.py` (RST inline-literal site + `exec_cmd`
  parallel surface)
- `docs/source/{conf.py,index.rst,api/index.rst}` (sphinx config +
  toctree)
- Repo root: `Makefile`, `README.md`, `CHANGELOG.md`, `CONTRIBUTORS.md`,
  `.github/CONTRIBUTING.md`, `pyproject.toml` (AUDIT POINT precedent)
- `.planning/codebase/CONVENTIONS.md`, `.planning/REQUIREMENTS.md`
- Prior phase artifacts: `.planning/phases/01-.../01-PATTERNS.md`,
  `.planning/phases/03-.../03-CONTEXT.md`,
  `.planning/phases/04-.../04-NOTE.md`

**Files scanned:** 18 (live) + 5 (prior-phase artifacts for
precedent) = 23

**Pattern extraction date:** 2026-05-07
