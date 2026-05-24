# Demo: Generate Extension - Features

Demonstrates the `features` support in the `generate` extension, which allows
`.generate.yml` templates to conditionally include/exclude files and prompt for
additional variables based on optional feature toggles.

The demo exercises **both** feature prompt modes:

- `prompt_mode: boolean` — the original single y/N toggle (`docker`,
  `docker_compose`).
- `prompt_mode: select` — a numbered multi-valued picker (`web_framework`),
  added for [issue #779][779].

## Template

The `templates/generate/webapp/` template defines:

- **Base variable:** `project_name`
- **Feature: `docker`** (boolean, default: enabled) — includes `Dockerfile`
  and `.dockerignore`, prompts for `python_version`
- **Feature: `docker_compose`** (boolean, default: enabled,
  **requires: docker**) — includes `docker-compose.yml`
- **Feature: `web_framework`** (select, default: `none`) — picks between
  None / Flask / FastAPI, controls `requirements.txt` + `wsgi.py`
  rendering and a silent `framework_version` variable

## Usage

Run from this directory:

```bash
# Generate with all defaults (docker=on, docker_compose=on, web_framework=none)
pdm run python myapp.py generate webapp /tmp/myproject --defaults

# Generate interactively (prompts for each variable and feature)
pdm run python myapp.py generate webapp /tmp/myproject

# Generate with --force to overwrite existing output
pdm run python myapp.py generate webapp /tmp/myproject --defaults --force
```

## Configuration

*templates/generate/webapp*

```yaml
---

variables:
    -   name: project_name
        prompt: "Project Name"
        default: "myproject"
        case: lower

features:
    -   name: docker
        prompt_mode: boolean
        default: true
        enabled:
            variables:
                -   name: python_version
                    prompt: "Python Version (for Docker)"
                    default: "3.13"
        disabled:
            ignore:
                - '.*Dockerfile.*'
                - '.*\.dockerignore.*'

    -   name: docker_compose
        prompt_mode: boolean
        default: true
        requires:
            - docker
        disabled:
            ignore:
                - '.*docker-compose.*'

    -   name: web_framework
        prompt_mode: select
        prompt: "Web Framework"
        default: "none"
        options:
            -   value: "none"
                prompt: "None — no web framework"
                ignore:
                    - '.*requirements\.txt.*'
                    - '.*wsgi\.py.*'
            -   value: "flask"
                prompt: "Flask Web Framework"
                variables:
                    -   name: framework_version
                        prompt: false
                        default: "3.0"
                ignore:
                    - '.*fastapi.*'
            -   value: "fastapi"
                prompt: "FastAPI Web Framework"
                variables:
                    -   name: framework_version
                        prompt: false
                        default: "0.115"
                ignore:
                    - '.*flask.*'
```

## Multi-Valued Feature (prompt_mode: select)

The `web_framework` feature uses the multi-valued `prompt_mode: select`
schema. Under the hood it delegates to `cement.utils.shell.Prompt` with
`numbered=True`, so the user sees a numbered picker:

```
Web Framework

1: None — no web framework
2: Flask Web Framework
3: FastAPI Web Framework

Enter the number for your selection:
```

**Schema keys** in select mode:

- `prompt_mode: select` — opt-in switch. The default is `'boolean'`
  (single y/N prompt with `enabled:` / `disabled:` blocks, as the
  `docker` and `docker_compose` features above use). The
  `prompt_mode` key MAY be omitted on boolean features for
  backward-compat with templates predating #779 — `prompt_mode:
  boolean` and omission are exactly equivalent.
- `prompt` — the heading text shown above the numbered list.
- `default` — REQUIRED. Must equal one of the `options[].value`
  entries (validated at config-load). Used both as the Prompt's
  default-when-user-hits-Enter and as the `--defaults` headless
  dispatch value.
- `options` — list of branches. Each branch:
  - `value:` (required) — the resolved feature state in the rendered
    template (`{{ web_framework }}` substitutes this string).
  - `prompt:` (optional) — the human-readable label shown in the
    numbered list. Falls back to `str(value)` if omitted. Must be
    unique across the feature's options.
  - `ignore:` / `exclude:` / `variables:` (all optional) — same
    vocabulary as the boolean-feature `enabled:` / `disabled:`
    blocks; merged into the template render context when this option
    is selected.

**Silent variables (`prompt: false`)**: a variable definition with
`prompt: false` is set to its `default` without rendering an
interactive prompt — useful for branch-specific metadata like a
framework's pinned version. The variable's `case` and `validate` (if
declared) still apply to the default value. Silent variables also
work outside `selected` branches (top-level `variables`).

**Headless run with `--defaults`**:

```bash
pdm run python myapp.py generate webapp /tmp/myproject --defaults
# → web_framework = "none" (feature-level default)
# → requirements.txt and wsgi.py both ignored (not rendered)
```

**Interaction with `requires:`**: a select-mode feature may declare
`requires: [other_feature]`. If a prerequisite resolves to false the
select feature is disabled and treated as "off" — none of its
`options` branches fire, and no `ignore` / `exclude` / `variables`
from any branch are applied. This mirrors the legacy boolean-feature
semantics: a disabled feature contributes nothing to the template
merge. If you need "off" to actively suppress files, attach the
`ignore` patterns to the prerequisite's own `disabled:` block instead
of an `options` branch.

[779]: https://github.com/datafolklabs/cement/issues/779

## What to Expect

**With all defaults** (docker on, docker_compose on, web_framework=none):

```text
/tmp/myproject/
├── .dockerignore
├── Dockerfile
├── README.md
├── app.py
└── docker-compose.yml
```

`web_framework=none` (the feature's default) ignores `requirements.txt`
and `wsgi.py`, so they do not appear in the rendered tree.

**With docker disabled** (docker_compose is auto-disabled via `requires`):

```text
/tmp/myproject/
├── README.md
└── app.py
```

No Dockerfile, no docker-compose.yml — disabling docker automatically
disables docker_compose because it requires docker.

**With web_framework=fastapi** (and other features default):

```text
/tmp/myproject/
├── .dockerignore
├── Dockerfile
├── README.md
├── app.py
├── docker-compose.yml
├── requirements.txt
└── wsgi.py
```

`requirements.txt` substitutes `fastapi==0.115` from the silent
`framework_version` variable on the fastapi branch.
