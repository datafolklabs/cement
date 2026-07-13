# Release Announcement — Cement 3.0.16

> **Status:** DRAFT — paste-ready copy. SENDING (mailing list / Slack /
> GitBook changelog) remains a HUMAN step tracked on the post-release
> checklist issue [#797](https://github.com/datafolklabs/cement/issues/797)
> (05.4 D-15 — out of scope for Phase 6).
>
> Body derived verbatim from the finalized `## 3.0.16` CHANGELOG.md
> highlights paragraph (D-03/D-14) — the single source of truth for what
> shipped. Do not re-summarize independently.

---

## Subject

Cement 3.0.16 released

## Body

Cement 3.0.16 is now available on PyPI.

This release modernizes Cement against the current Python ecosystem while
holding the 3.0.x public API stable. Python 3.8 and 3.9 are dropped (EOL) and
the supported matrix is now Python 3.10–3.14. Every deprecation in this release
is warn-only, with removals signposted for 3.2.0 so downstream apps have a
clear upgrade window. A new automated GitHub Actions release workflow replaces
the manual release checklist, and the `cement generate` project and
todo-tutorial templates are now fully typed, PEP 517-buildable, and green under
`make comply` and `make test` out of the box.

Upgrade:

```
pip install -U cement
```

Full details:

- GitHub Release: https://github.com/datafolklabs/cement/releases/tag/3.0.16
- Changelog: https://github.com/datafolklabs/cement/blob/main/CHANGELOG.md
- Docs: https://docs.builtoncement.com/

Docker images (linux/amd64 + linux/arm64) are published as
`datafolklabs/cement:3.0.16` / `:3.0` / `:3` / `:latest`.

Thanks to everyone who reported issues and contributed feedback this cycle.

---

## Sending checklist (human — issue #797)

- [ ] Mailing list
- [ ] Slack
- [ ] GitBook changelog page (builtoncement.com)
