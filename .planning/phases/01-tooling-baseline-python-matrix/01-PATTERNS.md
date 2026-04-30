# Phase 1: Tooling Baseline & Python Matrix - Pattern Map

**Mapped:** 2026-04-29
**Files analyzed:** 11 (10 modified + 1 deleted)
**Analogs found:** 11 / 11 (every file has a concrete analog — either
its own current-state block or a sibling Dockerfile pair)

> **Phase character:** This is a tooling/config phase, not a feature
> phase. There is no "create new file" surface — every file is an
> in-place edit (or a deletion). Therefore the "analog" for each file
> is one of:
>
> 1. **The file's own current-state block** — current shape is the
>    pattern; target shape is articulated by RESEARCH.md and is the
>    direct edit. (`pyproject.toml`, `build_and_test.yml`, `Makefile`,
>    `docker-compose.yml`, `README.md`, `.travis.yml`)
> 2. **A sibling file** that already shows the target shape — direct
>    base-image substitution copy. (`docker/Dockerfile.dev-py310` is
>    the pattern that the two `cement/cli/templates/generate/*/`
>    Dockerfiles must mirror at the `FROM python:3.X-alpine` line; the
>    two template Dockerfiles also mirror each other identically.)
>
> The planner consumes this file as: "for each file, here is the exact
> current text, the exact target text, and the rationale for why the
> change is mechanical." No abstract pattern interpretation is needed.

## File Classification

| File | Role | Data Flow | Closest Analog | Match Quality |
|------|------|-----------|----------------|---------------|
| `pyproject.toml` (`[project] requires-python`) | config (project metadata) | n/a (declarative) | self — current line 19 | exact (in-place bump) |
| `pyproject.toml` (`[tool.ruff]`) | config (lint rule definition) | n/a (declarative) | self — current lines 71–90 | exact (in-place bump + rule-set codification) |
| `pyproject.toml` (`[tool.mypy]`) | config (type-check rule definition) | n/a (declarative) | self — current lines 109–136 | exact (in-place bump; one-line `python_version` change) |
| `pyproject.toml` (`[dependency-groups] dev`) | config (dev-dep version pinning) | n/a (declarative) | self — current lines 156–167 | exact (per-line pin updates) |
| `.github/workflows/build_and_test.yml` | config (CI matrix) | n/a (declarative) | self — current line 68 | exact (single-list edit) |
| `Makefile` (`dev` target) | config (dev-loop entry) | n/a (declarative recipe) | self — current line 16 | exact (single-line delete) |
| `docker-compose.yml` (`cement-py39` service) | config (compose service definition) | n/a (declarative) | self — current lines 56–61 | exact (block delete) — `cement-py310` block (lines 63–68) is the sibling pattern that demonstrates the surviving service shape |
| `docker/Dockerfile.dev-py39` | config (Docker image build) | n/a (declarative) | DELETED — `docker/Dockerfile.dev-py310` is the surviving sibling and the implicit pattern for what stays | exact (whole-file delete) |
| `cement/cli/templates/generate/todo-tutorial/Dockerfile` | config (user-facing scaffold template) | n/a (declarative) | sibling pair: `cement/cli/templates/generate/project/Dockerfile` AND `docker/Dockerfile.dev-py310` | exact (one-line `FROM` bump) |
| `cement/cli/templates/generate/project/Dockerfile` | config (user-facing scaffold template) | n/a (declarative) | sibling pair: `cement/cli/templates/generate/todo-tutorial/Dockerfile` AND `docker/Dockerfile.dev-py310` | exact (one-line `FROM` bump) |
| `README.md` (Python-version prose) | docs (user-facing) | n/a (prose) | self — current lines 45, 136, 142, 152, 154 | exact (prose edits) |
| `.travis.yml` | config (legacy CI) | n/a (declarative) | self — current lines 15–28 | exact (delete file, OR drop 3.8/3.9 entries — recommend delete; see RESEARCH.md Pitfall 7) |

> **Source-tree fallout files** (`cement/**/*.py`, `tests/**/*.py`):
> Listed below in § "Source-Code Lint/Type Fallout". The analog for
> each fix is the nearest sibling file that already conforms (e.g., a
> non-violating `from pytest import raises` import block elsewhere in
> `tests/`). The planner walks ruff/mypy output for these in Step 2.

## Pattern Assignments

### `pyproject.toml` — `[project] requires-python` (config, declarative)

**Analog:** self, line 19

**Current state** (`pyproject.toml:19`):

```toml
requires-python = ">=3.9"
```

**Target state** (Step 1, D-05):

```toml
requires-python = ">=3.10"
```

**Why mechanical:** Single-line bump. No conditional logic, no syntax
elsewhere keys off this value at runtime — pip/PDM read it for
install-gating only. Verified by grep: this is the only
`requires-python` directive in the repo.

---

### `pyproject.toml` — `[tool.ruff]` (config, declarative — RULE-SET CODIFICATION)

**Analog:** self, lines 71–90

**Current state** (`pyproject.toml:71-90`):

```toml
[tool.ruff]
target-version = "py39"
line-length = 100
indent-width = 4
exclude = [
    ".git",
    "cement/cli/templates",
    "cement/cli/contrib"
]
include = [
    "cement/**/*.py",
    "tests/**/*.py"
]

[tool.ruff.lint]
preview = true
extend-select = ["E", "F", "W"]
ignore = []
fixable = ["ALL"]
unfixable = []
```

**Target state** (Step 1 D-05 + Step 2 D-06/D-08/D-09 — see
RESEARCH.md § "Hybrid Codification Pattern" and "Code Examples / Final
pyproject.toml shape"):

```toml
[tool.ruff]
target-version = "py310"            # was "py39"  (D-05, Step 1)
line-length = 100
indent-width = 4
exclude = [
    ".git",
    "cement/cli/templates",
    "cement/cli/contrib"
]
include = [
    "cement/**/*.py",
    "tests/**/*.py"
]

[tool.ruff.lint]
# AUDIT POINT (D-08): re-review on every ruff bump. New rules added
# by ruff to a selected family fire as CI failures, forcing a
# deliberate add-with-comment to `ignore` or a fix. See Phase 1
# RESEARCH.md.
preview = false                     # was true  (D-09, Step 2)
extend-select = [
    "E", "F", "W",                  # already enabled
    "B",                            # flake8-bugbear (NEW, D-06)
    "I",                            # isort (NEW, D-06)
    "A",                            # flake8-builtins (NEW, D-06)
    "C90",                          # mccabe (NEW, D-06)
    "N",                            # pep8-naming (NEW, D-06)
    "PT",                           # flake8-pytest-style (NEW, D-06)
    "T20",                          # flake8-print (NEW, D-06)
    "YTT",                          # flake8-2020 (NEW, D-06)
]
ignore = [
    # AUDIT POINT (D-08): each entry MUST have a one-line
    # justification. Empty list is the green-baseline goal.
]
fixable = ["ALL"]                   # unchanged
unfixable = []                      # unchanged
```

**Why this is the pattern (not just a substitution):** The
`extend-select` block is the load-bearing payload of TOOL-04. Every
new family added here is a deliberate decision; every rule that ruff
later moves *into* one of these families will surface as CI failure
on the next `pdm update`, forcing it through the audit-point. This
inverts the current implicit-drift posture (`preview = true` +
narrow family list = silent absorption of preview-graduated rules)
into an explicit-drift posture (`preview = false` + broader-but-named
family list + audit-point comments = deliberate engagement).

**Sequencing note:** `target-version = "py310"` lands in the Step 1
D-05 atomic commit; the rest of this block (preview flip + family
additions + audit comments) lands in the Step 2 `chore: bump ruff`
commit per D-15 ("pin and bump are coupled — never split").

---

### `pyproject.toml` — `[tool.mypy]` (config, declarative)

**Analog:** self, lines 109–136

**Current state** (`pyproject.toml:109-136`):

```toml
[tool.mypy]
python_version = "3.9"
disallow_untyped_calls = true
disallow_untyped_defs = true
disallow_any_unimported = false
disallow_incomplete_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
strict_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true

disable_error_code = [
    # disable as MetaMixin/Meta is used everywhere and triggers this
    "attr-defined",
]

files = [
    "cement/",
    # "tests/"
]
exclude = """(?x)(
    ^cement/cli/templates |
    ^.git/ |
    ^tests
  )"""
```

**Target state** (Step 1 D-05 changes line 110 only; Step 2
`chore: bump mypy` adds the audit-point comment per D-08):

```toml
[tool.mypy]
python_version = "3.10"             # was "3.9"  (D-05)
# AUDIT POINT (D-08+D-11): strictness knobs deliberately enumerated,
# NOT `strict = true`. Adding a knob is a deliberate decision. mypy
# bumps that introduce new strict defaults will fail CI.
disallow_untyped_calls = true
# (rest of strictness knobs unchanged per D-11)
disallow_untyped_defs = true
disallow_any_unimported = false
disallow_incomplete_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
strict_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true

disable_error_code = ["attr-defined"]  # MetaMixin/Meta — unchanged

files = ["cement/"]                    # tests excluded (D-10) — unchanged
exclude = """(?x)(
    ^cement/cli/templates |
    ^.git/ |
    ^tests
  )"""
```

**Why mechanical (per D-11):** Only `python_version` changes value.
Every other strictness knob retains its current setting. The only new
*content* is the AUDIT POINT comment (added in the Step 2
`chore: bump mypy` commit alongside the version pin per D-15) — no
strictness changes. D-10 preserves `tests/` exclusion exactly.

---

### `pyproject.toml` — `[dependency-groups] dev` (config, declarative)

**Analog:** self, lines 156–167

**Current state** (`pyproject.toml:156-167`):

```toml
[dependency-groups]
dev = [
    "pytest>=4.3.1",
    "pytest-cov>=2.6.1",
    "coverage>=4.5.3",
    "mypy>=1.9.0",
    "ruff>=0.3.2",
    "mock>=5.1.0",
    "pypng>=0.20220715.0",
    "requests>=2.31.0",
    "commitizen>=4.10.1",
]
```

**Target state** (Step 2 — pins land coupled to their respective
`chore: bump <tool>` commits per D-15):

```toml
[dependency-groups]
dev = [
    "pytest>=9.0.3",                # was >=4.3.1  (D-12: floor)
    "pytest-cov>=7.1.0",            # was >=2.6.1  (D-12: floor)
    "coverage>=7.13.5",             # was >=4.5.3  (D-12: floor)
    "mypy~=1.20.2",                 # was >=1.9.0  (D-12: ~=)
    "ruff~=0.15.12",                # was >=0.3.2  (D-12: ~=)
    "mock>=5.1.0",                  # unchanged
    "pypng>=0.20220715.0",          # unchanged
    "requests>=2.31.0",             # unchanged
    "commitizen>=4.10.1",           # unchanged
]
```

**D-12 hybrid pattern at a glance:** `~=` (compatible-release) on
`ruff` and `mypy` because they evolve fast and rule sets shift on
minor bumps; `>=` (floor) on `pytest`, `pytest-cov`, `coverage`,
`mock`, `pypng`, `requests`, `commitizen` because they break rarely.
Targeted control where the actual drift risk lives.

**Sequencing per D-15:** ruff pin (`ruff~=0.15.12`) lands in the
`chore: bump ruff to 0.15` commit; mypy pin (`mypy~=1.20.2`) lands in
the `chore: bump mypy to 1.20` commit; pytest+pytest-cov+coverage
floors land in the final `chore: bump pytest+pytest-cov+coverage`
commit. Order: ruff → mypy → pytest per D-03.

---

### `.github/workflows/build_and_test.yml` (config, declarative)

**Analog:** self, line 68

**Current state** (`.github/workflows/build_and_test.yml:68`):

```yaml
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]
```

**Target state** (Step 1, D-05 atomic commit):

```yaml
        python-version: ["3.10", "3.11", "3.12", "3.13", "3.14", "pypy3.10"]
```

**Why mechanical:** Single list-element delete. No other line in this
workflow file references Python 3.9 (verified by grep). The
`python-version: "3.x"` directives at lines 27 and 48 are
`actions/setup-python` defaults that resolve to the latest stable
Python 3 — they are version-floor-agnostic and need no edit.

---

### `Makefile` — `dev` target (config, declarative recipe)

**Analog:** self, line 16

**Current state** (`Makefile:13-21`):

```makefile
dev:
	docker compose up -d
	docker compose exec cement pdm install
	docker compose exec cement-py39 pdm install
	docker compose exec cement-py310 pdm install
	docker compose exec cement-py311 pdm install
	docker compose exec cement-py312 pdm install
	docker compose exec cement-py313 pdm install
	docker compose exec cement /bin/bash
```

**Target state** (Step 1, D-05 atomic commit):

```makefile
dev:
	docker compose up -d
	docker compose exec cement pdm install
	docker compose exec cement-py310 pdm install
	docker compose exec cement-py311 pdm install
	docker compose exec cement-py312 pdm install
	docker compose exec cement-py313 pdm install
	docker compose exec cement /bin/bash
```

**Why mechanical:** Single-line delete (`cement-py39` line, current
line 16). The remaining lines are unchanged. Note: `cement-py314`
service is not currently in the Makefile dev loop — that's a future
addition Phase 2 may handle if the docker-compose service is added;
not in Phase 1 scope.

---

### `docker-compose.yml` — `cement-py39` service (config, declarative)

**Analog:** self, lines 56–61 (target deletion); sibling pattern at
lines 63–68 (`cement-py310` service) shows the shape that survives.

**Current state — block to delete** (`docker-compose.yml:56-61`):

```yaml
  cement-py39:
    <<: *DEFAULTS
    image: "cement:dev-py39"
    build:
      context: .
      dockerfile: docker/Dockerfile.dev-py39
```

**Sibling pattern that survives** (`docker-compose.yml:63-68`):

```yaml
  cement-py310:
    <<: *DEFAULTS
    image: "cement:dev-py310"
    build:
      context: .
      dockerfile: docker/Dockerfile.dev-py310
```

**Target state** (Step 1, D-05 atomic commit): delete the
`cement-py39:` block (lines 56–61) entirely. The `cement-py310:`
block becomes the new lowest-Python-version service in the file.

**Why mechanical:** Whole-block delete with a clean sibling pattern
(`cement-py310`, `cement-py311`, etc.) demonstrating that the rest of
the compose file is consistent.

---

### `docker/Dockerfile.dev-py39` (config, declarative — DELETE)

**Analog:** sibling `docker/Dockerfile.dev-py310` (the file that
survives and demonstrates the pattern we're keeping)

**Current state — file being deleted** (`docker/Dockerfile.dev-py39`,
all 28 lines):

```dockerfile
FROM python:3.9-alpine
LABEL MAINTAINER="BJ Dierkes <derks@datafolklabs.com>"
ENV PS1="\[\e[0;33m\]|> cement-py39 <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /src
RUN apk update \
    && apk add libmemcached-dev \
        gcc \
        musl-dev \
        cyrus-sasl-dev \
        zlib-dev \
        make \
        vim \
        bash \
        git \
        libffi \
        libffi-dev \
        openssl-dev \
        jq \
        pipx \
    && ln -sf /usr/bin/vim /usr/bin/vi
RUN pipx install pdm
COPY . /src
COPY docker/vimrc /root/.vimrc
COPY docker/bashrc /root/.bashrc
RUN pdm install
CMD ["/bin/bash"]
```

**Sibling pattern (`docker/Dockerfile.dev-py310`) that survives —
identical aside from FROM and PS1 prompt:**

```dockerfile
FROM python:3.10-alpine
LABEL MAINTAINER="BJ Dierkes <derks@datafolklabs.com>"
ENV PS1="\[\e[0;33m\]|> cement-py310 <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /src
RUN apk update \
    && apk add libmemcached-dev \
        ... [identical body]
```

**Target state** (Step 1, D-05 atomic commit): `git rm
docker/Dockerfile.dev-py39`.

**Why mechanical:** Whole-file deletion. The sibling Dockerfile.dev
files (`-py310`, `-py311`, `-py312`, `-py313`, `-py314`) show the
pattern that remains; nothing else references `Dockerfile.dev-py39`
except the `docker-compose.yml` block being deleted in lockstep above.

---

### `cement/cli/templates/generate/todo-tutorial/Dockerfile` (config, user-facing scaffold)

**Analog (sibling pair):** `cement/cli/templates/generate/project/Dockerfile`
(must change identically to this file). Secondary analog:
`docker/Dockerfile.dev-py310` (`FROM python:3.10-alpine` is the
target value).

**Current state**
(`cement/cli/templates/generate/todo-tutorial/Dockerfile`, line 1):

```dockerfile
FROM python:3.9-alpine
LABEL MAINTAINER="Your Name <you@yourdomain.com>"
ENV PS1="\[\e[0;33m\]|> todo <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
... [rest of file unchanged]
```

**Target state** (Step 1, D-05 atomic commit):

```dockerfile
FROM python:3.10-alpine
LABEL MAINTAINER="Your Name <you@yourdomain.com>"
ENV PS1="\[\e[0;33m\]|> todo <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
... [rest of file unchanged]
```

**Why mechanical:** Single-line `FROM` bump. The
`docker/Dockerfile.dev-py310` sibling proves `python:3.10-alpine` is a
known-working base image in this project. **User-facing impact:** new
apps scaffolded via `cement generate` will produce
`python:3.10-alpine` Dockerfiles — flag in the eventual 3.0.16
changelog (Phase 6 DOCS-03).

---

### `cement/cli/templates/generate/project/Dockerfile` (config, user-facing scaffold)

**Analog (sibling pair):** `cement/cli/templates/generate/todo-tutorial/Dockerfile`
(must change identically to this file).

**Current state**
(`cement/cli/templates/generate/project/Dockerfile`, line 1):

```dockerfile
FROM python:3.9-alpine
LABEL MAINTAINER="{{ creator }} <{{ creator_email }}>"
ENV PS1="\[\e[0;33m\]|> {{ label }} <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
... [rest of file unchanged]
```

**Target state** (Step 1, D-05 atomic commit):

```dockerfile
FROM python:3.10-alpine
LABEL MAINTAINER="{{ creator }} <{{ creator_email }}>"
ENV PS1="\[\e[0;33m\]|> {{ label }} <| \[\e[1;35m\]\W\[\e[0m\] \[\e[0m\]# "
... [rest of file unchanged]
```

**Why mechanical:** Identical edit to the sibling
`todo-tutorial/Dockerfile`. **Treat the two template Dockerfiles as
one analog pair** — they MUST change in lockstep. If only one is
bumped, the planner has split the D-05 atomic commit and violated
"ALL 3.9 traces simultaneously."

---

### `README.md` — Python-version prose (docs, prose)

**Analog:** self, current lines 45, 136, 142, 152, 154

**Current state** (excerpts):

```markdown
- Tested on Python 3.9+
```
(line 45)

```markdown
The latest stable version of Python 3 is the default, and target
version accessible as the `cement` container within Docker Compose.
For testing against alternative versions of python, additional
containers are created (ex: `cement-py39`, `cement-py310`, etc).
```
(line 136)

```
cement_cement-py39_1    /bin/bash                        Up
```
(line 142)

```
$ docker-compose exec cement-py39 /bin/bash

|> cement-py39 <| src #
```
(lines 152, 154)

**Target state** (Step 1, D-05 atomic commit):

- Line 45: `- Tested on Python 3.10+`
- Line 136: replace `cement-py39` with `cement-py310` (or drop the
  parenthetical example entirely)
- Lines 142, 152, 154: drop the `cement-py39` example block, OR
  replace with `cement-py310` to keep parity with the surviving
  containers. **Recommend replace with py310** to preserve the
  example shape that downstream readers learn from.

**Why mechanical:** Prose-only edit. No code or directive change. The
"recommend replace" framing matters because cement's docs are
user-facing and the example is teaching the docker-compose-exec
pattern, not advocating for py39 specifically.

---

### `.travis.yml` (config, legacy CI — RECOMMEND DELETE)

**Analog:** self, lines 15–28 (the 3.8 and 3.9 matrix entries that
must go either way)

**Current state** (`.travis.yml:13-28`, the matrix block):

```yaml
matrix:
  include:
    - python: "3.8"
      dist: "focal"
      sudo: true
      env:
        - DOCKER_COMPOSE_VERSION=v2.17.3
        - SMTP_HOST=localhost
        - SMTP_PORT=1025
    - python: "3.9"
      dist: "focal"
      sudo: true
      env:
        - DOCKER_COMPOSE_VERSION=v2.17.3
        - SMTP_HOST=localhost
        - SMTP_PORT=1025
    - python: "3.10"
      ... [rest continues through 3.13]
```

**Target state** (Step 1, D-05 atomic commit) — RESEARCH.md Pitfall 7
recommends **delete the file entirely**. Travis CI is no longer
cement's primary or secondary CI; GitHub Actions is. The fallback is
to drop the 3.8 and 3.9 matrix entries (lines 15–28) in lockstep with
`build_and_test.yml`.

**Why mechanical:** Whole-file `git rm`. Either action satisfies
D-05's "ALL 3.9 traces simultaneously." Recommend deletion because
maintaining a second CI definition that is not actually run is dead
infrastructure and a future-grep liability.

---

## Source-Code Lint/Type Fallout

**Step 2 only.** Each is a one-commit-per-rule-family fix per D-04.
The "analog" for each fix is the closest non-violating file already
in the repo. Concrete fallout numbers and rule codes from RESEARCH.md
§ "Ruff Family Selection (D-06 Recommendation)".

| Family | Code | Violations | Action | Fix Pattern Source |
|--------|------|-----------:|--------|---------------------|
| flake8-bugbear | B007 | 17 | `for x in ...:` → `for _ in ...:` (where x unused) | Trivial mechanical fix; no analog needed. |
| flake8-bugbear | B904 | 8 | Add `from err` to re-raises inside except | Look at `cement/core/exc.py` and `cement/core/foundation.py` for already-correct `raise FrameworkError(...) from e` examples if any exist; else mechanical add. |
| isort | I001 | 80 | `make comply-ruff-fix` (auto-fix `[*]`) | Auto-fix, no analog needed. |
| flake8-builtins | A001/A002 | 18 | Rename or `# noqa: A001` with audit comment | Case-by-case; framework intentionally shadows builtins in handler kwargs (e.g., `type` parameter). RESEARCH.md notes attrs ignores this family for the same reason. Recommend per-file-ignore or rename based on call-site review. |
| mccabe | C901 | 12 | Recommend absorb in `[tool.ruff.lint] ignore = ["C901"]` with audit comment pointing to Phase 3 REFACTOR-01 (per D-13 strict-minimum) | RESEARCH.md Open Question 3 explicitly recommends this. |
| pep8-naming | N806 | 6 | Per-file-ignore for `tests/**/*.py` if test casing intentional | RESEARCH.md Pitfall 6 documents the pattern: `[tool.ruff.lint.per-file-ignores] "tests/**/*.py" = ["N806"]`. |
| flake8-pytest-style | PT013 | 14 | `import pytest` → `from pytest import raises` etc. | Pattern source: `tests/core/test_exc.py` line ~ `from pytest import raises` (RESEARCH.md cites this as the existing convention). |
| flake8-print | T20 | 8 | Remove or `# noqa: T201` for intentional CLI `print()` | Audit each site; CLI templates and scripts are likely sources. |
| flake8-2020 | YTT203 | 1 | Fix stale `sys.version_info[0] >= 3 and sys.version_info[1] >= 4` shim at `tests/ext/test_ext_argparse.py:13` | The shim checks for Python 3.4+, so `ARGPARSE_SUPPORTS_DEFAULTS = True` unconditionally is the fix. **NOT a Phase 1 Step 1 edit** — surfaces only after `YTT` is added to `extend-select` in the ruff bump commit. |

### mypy fallout (TOOL-02, Step 2 `chore: bump mypy` + `fix(types):`)

| File | Line | Error | Fix Approach |
|------|-----:|-------|--------------|
| `cement/core/handler.py` | 392 | union-attr | Targeted fix only. Sibling pattern: lines 385, 387, 388, 391, 393 already use `# type: ignore` for the MetaMixin/Meta pattern. Mirror that approach OR add a narrowing assertion. RESEARCH.md verified this is the only fallout. |

**Step 2 commit shape per D-03 + D-04** (verbatim from RESEARCH.md
§ "Pattern 1: One Commit Per Rule Family"):

```
chore: bump ruff to 0.15
fix(lint): resolve I001 unsorted-imports (auto-fix)
fix(lint): resolve B007 unused-loop-variable
fix(lint): resolve B904 raise-without-from
fix(lint): resolve B005/B006/B011 misc bugbear
fix(lint): resolve A001/A002 builtin-shadowing
fix(lint): resolve C901 complex-structure
fix(lint): resolve N806/N801/N802 naming
fix(lint): resolve PT013/PT012 pytest-style
fix(lint): resolve T201 print-statements
fix(lint): resolve YTT203 sys-version-info
chore: bump mypy to 1.20
fix(types): resolve union-attr in core/handler.py
chore: bump pytest+pytest-cov+coverage
```

---

## Shared Patterns

### Pattern: Conventional Commits with 78-char wrap (CLAUDE.md)

**Source:** `CLAUDE.md` § "Commit Conventions"
**Apply to:** Every commit in Step 1 and Step 2.

```
chore: drop python 3.9 from supported matrix     <- subject ≤ 78 chars
                                                    blank line
This commit removes Python 3.9 from `requires-python`, the          <- body ≤ 78 chars
ruff target-version, the mypy python_version, the GitHub Actions    <- body ≤ 78 chars
matrix, the Makefile dev target, the docker-compose service, and    <- body ≤ 78 chars
the two generate-template Dockerfiles.                              <- body ≤ 78 chars

Co-Authored-By: ...
```

Use `make commit` (`pdm run cz commit`) for interactive authoring
per CLAUDE.md.

### Pattern: AUDIT POINT codification comment (D-08)

**Source:** RESEARCH.md § "Hybrid Codification Pattern" — the
canonical text is reproduced in this PATTERNS.md under the
`pyproject.toml [tool.ruff.lint]` and `[tool.mypy]` sections.

**Apply to:** Both `[tool.ruff.lint]` (above the `preview = false`
line) and `[tool.mypy]` (above the strictness knobs). The comment
text MUST cite "Phase 1 RESEARCH.md" or "Phase 1 D-08" so future
auditors find the rationale without spelunking.

```toml
# AUDIT POINT (D-08): re-review on every <tool> bump. New rules added
# by <tool> to a selected family fire as CI failures, forcing a
# deliberate add-with-comment to `ignore` or a fix. See Phase 1
# RESEARCH.md.
```

**Why this is shared:** Both ruff and mypy share the same drift-
detection pattern. The comment text is near-identical between the
two; only the tool name and the specific knob list change. This is
the structural payload of TOOL-04 — the *only* place rule membership
can change is via a deliberate edit to `pyproject.toml`.

### Pattern: D-15 coupling — version pin lands with version bump

**Source:** CONTEXT.md D-15.
**Apply to:** Step 2 commits.

- `chore: bump ruff to 0.15` MUST also flip `ruff>=0.3.2` →
  `ruff~=0.15.12` AND set `preview = false` AND extend `extend-select`
  in the same commit. Pin, preview flip, family addition, and audit
  comment are one atomic unit per D-08 + D-09 + D-15.
- `chore: bump mypy to 1.20` MUST also flip `mypy>=1.9.0` →
  `mypy~=1.20.2` in the same commit.
- `chore: bump pytest+pytest-cov+coverage` MUST flip all three floor
  pins in one commit (`pytest>=9.0.3`, `pytest-cov>=7.1.0`,
  `coverage>=7.13.5`) since they are floor-only and independent of
  rule-set codification.

### Pattern: Verification gates per commit (RESEARCH.md § "Sampling Rate")

**Source:** RESEARCH.md § "Validation Architecture / Sampling Rate".
**Apply to:** Every commit in Step 1 and Step 2 — local equivalent of
CI gate before push.

```bash
# Per ruff-fix commit (Step 2)
pdm run ruff check cement/ tests/

# Per mypy-fix commit (Step 2)
pdm run mypy

# Per pytest-bump commit (Step 2)
pdm run pytest tests/core

# Per step boundary (Step 1 → Step 2 and end of Step 2)
make comply && make test

# Phase gate (after PR opens)
gh pr checks <PR-NUMBER>
```

---

## No Analog Found

**None.** Every file in this phase has either:

1. A current-state block in itself (in-place edit), or
2. A sibling that demonstrates the surviving target shape
   (`Dockerfile.dev-py310` for `Dockerfile.dev-py39` deletion;
   `cement-py310` compose service for `cement-py39` deletion;
   sibling-pair Dockerfiles for the two generate-templates).

---

## Metadata

**Analog search scope:** repo root + `.github/workflows/` +
`docker/` + `cement/cli/templates/generate/*/`. Search exhausted;
RESEARCH.md § "Runtime State Inventory" is the verified-grep
trace inventory and matches my reads.

**Files scanned (read into context):**
- `pyproject.toml` (full, lines 1–168)
- `.github/workflows/build_and_test.yml` (full, lines 1–99)
- `Makefile` (full, lines 1–88)
- `docker-compose.yml` (full, lines 1–90)
- `docker/Dockerfile.dev-py39` (full, lines 1–28)
- `docker/Dockerfile.dev-py310` (full, lines 1–29 — sibling
  pattern)
- `cement/cli/templates/generate/todo-tutorial/Dockerfile` (full,
  lines 1–19)
- `cement/cli/templates/generate/project/Dockerfile` (full, lines
  1–11)
- `.travis.yml` (full, lines 1–66)
- `README.md` (lines 40–60, 130–164 — the prose to edit)
- `tests/ext/test_ext_argparse.py` (lines 1–20 — YTT203 site)
- `cement/core/handler.py` (lines 385–399 — mypy union-attr site)

**Analog directory enumeration:**
- `docker/` — confirmed `Dockerfile.dev-py39` exists alongside
  `-py310`, `-py311`, `-py312`, `-py313`, `-py314` siblings.
- `cement/cli/templates/generate/` — confirmed only the two
  template Dockerfiles exist; both are `python:3.9-alpine`.

**Pattern extraction date:** 2026-04-29
