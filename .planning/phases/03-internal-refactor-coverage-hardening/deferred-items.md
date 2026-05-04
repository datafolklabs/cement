# Phase 03 — Deferred Items

Items discovered during Wave 3 execution that are OUT OF SCOPE for this plan
(not caused by the task changes) but worth recording for future cleanup.

## Pre-existing duplicate `LOG = minimal_logger(__name__)` — RESOLVED

- **File:** `cement/ext/ext_daemon.py:20-21` (post-Wave-4: lines 18-19)
- **Issue:** Duplicate `LOG = minimal_logger(__name__)` lines (one at line 20,
  one at line 21). Second assignment is a no-op overwrite of the first.
- **Discovered:** Wave 3, UP004 sweep (was already present at commit
  `0375779b` before Wave 3 started).
- **Original disposition:** Deferred as "no functional impact (idempotent)".
- **Resolution (post-Wave-9 maintenance):** **Disposition was wrong.** The
  duplicate had a real functional impact: `logging.getLogger(namespace)`
  returns the same backend logger per name, but `MinimalLogger.__init__`
  unconditionally called `self.backend.addHandler(console)`, so the second
  `LOG = minimal_logger(__name__)` line attached a second `StreamHandler`
  to the shared backend. Any debug emit on the `cement.ext.ext_daemon`
  namespace would print twice. The latent bug also affected any other
  caller that re-created a `MinimalLogger` for the same namespace
  (e.g. `tests/core/test_foundation.py` calls `minimal_logger(__name__)`
  six times across different test functions, all with the same
  `__name__`). Fixed in commit `df1773bf` by (a) removing the duplicate
  line in `ext_daemon.py` and (b) guarding `MinimalLogger.__init__`'s
  `addHandler` call on `not self.backend.handlers` for full idempotency.
  Regression test at
  `tests/utils/test_misc.py::test_minimal_logger_does_not_duplicate_handlers`.

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
