# Phase 03 — Deferred Items

Items discovered during Wave 3 execution that are OUT OF SCOPE for this plan
(not caused by the task changes) but worth recording for future cleanup.

## Pre-existing duplicate `LOG = minimal_logger(__name__)`

- **File:** `cement/ext/ext_daemon.py:20-21`
- **Issue:** Duplicate `LOG = minimal_logger(__name__)` lines (one at line 20,
  one at line 21). Second assignment is a no-op overwrite of the first.
- **Discovered:** Wave 3, UP004 sweep (was already present at commit
  `0375779b` before Wave 3 started).
- **Disposition:** Defer. Pre-existing, not caused by Wave 3 changes. No
  functional impact (idempotent). Worth a one-line `chore` cleanup in a
  future tech-debt phase or alongside the Phase 03 D-15 pragma audit pass.

## D-19 line drift recorded

- **File:** `cement/core/foundation.py`
- **Note:** CONTEXT.md D-19 / 03-PATTERNS.md cite the protected
  `.format(**template_dict)` callsites at lines 1359, 1364, 1372, 1377,
  1385, 1390, 1478, 1483, 1488, 1492, 1553, 1558, 1563, 1567. After Wave 3
  UP006/UP007/UP045 line-shifts the actual current line numbers are 1353,
  1358, 1366, 1371, 1379, 1384, 1472, 1477, 1482, 1486, 1547, 1552, 1557,
  1561 (still 14 sites; semantics identical). The literal CONTEXT.md text
  is now stale; future references should grep for the pattern rather than
  cite line numbers.

## CONTEXT.md template.py:359+ reference is incorrect

- **File:** `cement/core/template.py`
- **Note:** CONTEXT.md D-19 cites "template.py:359+" as a protected
  `.format(**template_dict)` zone. The actual file has ZERO `.format()`
  callsites. Line 359 corresponds to a `def load()` method body unrelated
  to template substitution. Either the CONTEXT.md reference is outdated or
  it referred to printf-style `%` LOG.debug sites (lines 332, 346, 350)
  that UP031 correctly converted (no template-substitution semantics —
  these are pure log statements). No D-19 violation occurred.
