---
quick_id: 260524-g47
type: verification
status: passed
verified_at: 2026-05-24
---

# Quick Task 260524-g47: Verification Report

**Phase Goal:** Extend `cement/ext/ext_generate.py` to support multi-valued
feature prompts (`prompt_mode: select`) per GH Issue #779.

**Status:** PASSED — every must-have verified; coverage gate green;
compliance green; public-API audit clean; all 4 code-review findings
addressed; backward compatibility intact.

## Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| T1 | `prompt_mode: select` explicit opt-in; legacy path byte-identical when absent | VERIFIED | `cement/ext/ext_generate.py:54-56` — `mode = feature.get('prompt_mode'); if mode is None: continue`. Legacy `_resolve` branch at lines 160-176 unchanged in semantics (renamed `FeaturePrompt`→`BoolFeaturePrompt`, `p`/`val`→`bp`/`bval` for mypy variable-retyping safety only). All test1–test15 fixtures unchanged on disk and pass. |
| T2 | `selected:` is list of dicts with explicit `value:` key (with `str()` coercion) | VERIFIED | `ext_generate.py:71-80` — iterates `selected`, raises `ValueError` on missing `value:`, builds `values: list[str] = [str(branch['value']) for branch in selected]`. Pitfall C handled via `str()` cast at lines 80, 153, 199. |
| T3 | Silent vars via `prompt: false`; case+validate still apply to default; str-coerce post-fix | VERIFIED | `ext_generate.py:264-275` — `if var['prompt'] is False:` short-circuit asserts `default is not None`, then `val = str(var['default'])`. Existing post-resolve case/validate block at lines 294-305 applies unchanged. Test29 (`silent_flag: false default + case: upper → "FALSE"`) covers the str-coerce. |
| T4 | Fail-fast: ValueError on `prompt_mode+enabled/disabled` collision; AssertionError on unmatched input | VERIFIED | Collision: `ext_generate.py:61-65`. Unmatched: `ext_generate.py:152-158` — `assert val in valid_values` sits OUTSIDE the pragma block (no `# pragma: nocover` annotation on the assert line; verified by `grep -B2 "must be one of"`). |
| T5 | (Post-fix) `default:` is REQUIRED for select-mode features (WR-01 closed) | VERIFIED | `ext_generate.py:86-89` — `if feature.get('default') is None: raise ValueError(... has no 'default' value)`. Test28 (`test_generate_features_select_missing_default`) exercises it. |

**Score:** 5/5 truths verified.

## Coverage-Gate Landmines (RESEARCH.md §4 — all 13 + 2 post-fix)

| # | Branch | Test |
|---|--------|------|
| 1 | `if mode is None: continue` (legacy early-out) | implicit via test6..test15 (pre-existing) |
| 2 | `if mode != 'select': raise ValueError` | `test_generate_features_select_invalid_prompt_mode` (test18) |
| 3 | collision raise | `test_generate_features_select_collision` (test17) |
| 4 | empty `selected` raise | `test_generate_features_select_empty_selected` (test26) |
| 5 | missing `value:` raise | `test_generate_features_select_missing_value` (test21) |
| 6 | default-not-in-values raise | `test_generate_features_select_default_not_in_values` (test20) |
| 7 | `--defaults` select assignment | `test_generate_features_select_defaults` (test16) |
| 8 | merge walks `selected` for matching value | `test_generate_features_select_defaults` (test16, implicit via file presence) |
| 9 | `block.get('variables') or []` null-coalesce on select path | `test_generate_features_select_null_variables` (test24) + `test_generate_features_legacy_null_variables` (test23, legacy path) |
| 10 | variable-loop `prompt is False` short-circuit | `test_generate_features_select_silent_variable` (test19) + `test_generate_features_top_level_silent_variable` (test22) |
| 11 | silent-var `default is not None` assert | `test_generate_features_select_no_default_branch` (test27) |
| 12 | top-level silent variable | `test_generate_features_top_level_silent_variable` (test22) |
| 13 | unmatched-input `assert val in valid_values` (NO pragma) | `test_generate_features_select_unmatched_input` (test16 + mocked Prompt returning "3") |
| +1 | post-validate `feature_states[name] = val` (interactive valid input) | `test_generate_features_select_interactive_match` (bonus, test16 + mocked Prompt returning "2") |
| +2 (WR-01) | `default is None` raise for select | `test_generate_features_select_missing_default` (test28) |
| +3 (WR-03) | silent-var `str()` coercion + case | `test_generate_features_silent_variable_non_str_default` (test29) |

**Coverage result:** `pdm run pytest --cov=cement.ext.ext_generate --cov-fail-under=100 tests/ext/test_ext_generate.py` → `cement/ext/ext_generate.py 205 0 100.00%` — `Required test coverage of 100% reached.`

## Backward-Compat Anchors

| Anchor | Status | Evidence |
|--------|--------|----------|
| test1..test15 fixtures unchanged on disk; all pre-existing tests pass | VERIFIED | `ls tests/data/templates/generate/` shows test1..test29; no edits to test1..test15. Pre-existing tests (test_generate, test_prompt, test_invalid_case, test_invalid_variable_value, test_no_default, test_clone, test_generate_from_template_dir, test_generate_default_command, test_filtered_sub_dirs, test_generate_features_{enabled,disabled,missing_name,requires_satisfied,requires_not_satisfied,requires_unknown,minimal,transitive_requires,requires_out_of_order,null_block}, test_generate_bad_template_module, test_generate_template_module_transitive_import_error) all pass. |
| `make audit-public-api` shows empty diff | VERIFIED | `make audit-public-api; echo "EXIT: $?"` → `EXIT: 0` with no stdout diff. |
| Demo `docker`+`docker_compose` blocks byte-identical (no `-` lines in diff against d0da2a4d^) | VERIFIED | `git diff d0da2a4d^..HEAD -- demo/generate-features/templates/generate/webapp/.generate.yml \| grep "^-" \| grep -v "^--- "` → zero lines. Only additions visible (lines 28-60 of diff). |

## Code-Review Follow-Up (3240d58d)

| # | Finding | Status |
|---|---------|--------|
| WR-01 | `default:` not required for select-mode → silent no-op under `--defaults` | RESOLVED — validation at `ext_generate.py:86-89` raises ValueError; `test_generate_features_select_missing_default` (test28) covers it. |
| WR-02 | Interactive prompt with `default=None` falls back to literal `"None"` | RESOLVED (dissolved by WR-01 fix — the `default is None` path is now unreachable at config time). |
| WR-03 | `case` on silent variable crashes on non-string YAML default | RESOLVED — `val = str(var['default'])` at `ext_generate.py:275`. `test_generate_features_silent_variable_non_str_default` (test29) exercises `default: false + case: upper → "FALSE"`. |
| WR-04 | `requires`-cascade silently drops select branches — undocumented | RESOLVED — demo README §"Multi-Valued Feature" (lines 144-151) documents: "If a prerequisite resolves to false the select feature is disabled and treated as 'off' — none of its `selected` branches run, and no `ignore`/`exclude`/`variables` from any branch are applied." |

## CONTEXT.md LOCKED Decisions

| Decision | Code Honors | Test |
|----------|-------------|------|
| A (collision) | `ext_generate.py:61-65` raises ValueError | `test_generate_features_select_collision` |
| B (unmatched input) | `ext_generate.py:156-158` raises AssertionError, no pragma | `test_generate_features_select_unmatched_input` |
| C (no default branch fallback; default must be in selected) | Validator at `ext_generate.py:86-94` (post-fix REQUIRES default + must be in values) | `test_generate_features_select_default_not_in_values` (test20) + `test_generate_features_select_missing_default` (test28) |
| D (`--defaults` dispatch) | `ext_generate.py:122-124` — `default = feature['default']; feature_states[name] = str(default)` | `test_generate_features_select_defaults` (test16) |

## Quality Gates

| Gate | Result |
|------|--------|
| `pdm run pytest --cov=cement.ext.ext_generate --cov-fail-under=100 tests/ext/test_ext_generate.py` | 205/205 statements, 100.00% coverage; ext_generate tests pass (10 failed only in test_ext_memcached/redis — pre-existing infra failures, services not running; identical to baseline d0da2a4d^) |
| `make comply` (ruff + mypy) | `All checks passed!` + `Success: no issues found in 51 source files` |
| `make audit-public-api` | Exit 0, no diff |
| Conventional Commits subjects ≤78 chars | All 6 commits: 64/69/72/68/67/67 chars |
| CHANGELOG entry under `## 3.0.15 - DEVELOPMENT` → `Features:` bucket, `[ext.generate]` tag, links #779 | VERIFIED at CHANGELOG.md:172-179; max line length 70 chars (all ≤78) |
| New tests count | 16 (RESEARCH.md §4 enumerated 13 + 1 bonus + 2 post-fix WR-01/WR-03) |

## Test Count

- `def test_*` total in `tests/ext/test_ext_generate.py`: 37
- Pre-existing (per RESEARCH.md): 21
- New: 16 (13 RESEARCH.md §4 mapping + 1 bonus `test_generate_features_select_interactive_match` + 1 WR-01 `test_generate_features_select_missing_default` + 1 WR-03 `test_generate_features_silent_variable_non_str_default`)

## Notes

- `.dockerignore` claim in SUMMARY verified — file is present at
  `demo/generate-features/templates/generate/webapp/.dockerignore` (149 bytes,
  already git-tracked from before this task).
- Memcached/Redis test failures (10) are pre-existing infrastructure
  failures from absent services; identical against the baseline commit
  (`d0da2a4d`). NOT introduced by this task. Out of scope.

---

_Verified: 2026-05-24_
_Verifier: Claude (gsd-verifier)_
