---
created: 2026-05-09T00:56:29.589Z
title: Document ext.generate optional features in GitBook (post-3.0.16)
area: docs
files:
  - cement/ext/ext_generate.py
  - demo/generate-features/
issue: 778
blocked_by: cement 3.0.16 release cut
---

## Problem

The new optional-features support in `cement.ext.ext_generate` (PR #768,
landing in 3.0.16) needs a developer-facing guide on the GitBook docs
at https://docs.builtoncement.com. Per the project convention,
Sphinx is API-reference only — narrative usage docs live in GitBook.

Tracked upstream as
[Issue #778](https://github.com/datafolklabs/cement/issues/778).

**Defer until after 3.0.16 cut** so docs land against released
behavior and the `pip install cement==3.0.16` example in the doc is
verifiable against the published artifact.

## Solution

When 3.0.16 ships:

1. Author the GitBook page under the existing `generate` extension
   section. Subsection: "Optional Features".
2. Cover the items in #778's "What the doc should cover" list:
   mental model, `.generate.yml` schema reference, CLI flow (with
   note on lazy interactive prompts), `features.<name>` Jinja2
   access, worked example pointer (`demo/generate-features/`),
   authoring checklist, pitfalls, ValueError validation behavior.
3. Verify the worked example by installing the released wheel
   (`pip install cement==3.0.16`) and running the demo against it.
4. Cross-link from the CHANGELOG `3.0.16` Features entry to the
   GitBook page once published.
5. Update PR #768's description (or a follow-up comment) with the
   GitBook link as the canonical doc pointer.
6. Close issue #778 with the GitBook URL.

Source material for the doc already exists in this conversation —
the primer written for the user covers ~90% of the content;
recycle that as the starting draft.
