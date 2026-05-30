# Demo: Generate Extension - Typed Variables

Demonstrates the unified typed-variable support in the `generate` extension,
which lets `.generate.yml` templates declare each variable's `type:`
(`string`, `boolean`, or `choice`), conditionally include/exclude files and
prompt for additional variables via `extend:`, and gate a variable on other
variables via `requires:`.

> **Schema note:** the legacy `features:` / `prompt_mode:` /
> `enabled:` / `disabled:` vocabulary has been removed. Everything is now a
> single `variables:` list where each entry carries a `type:`. A boolean or
> choice variable lands at the **top level** of the template context
> (`data[name]`), so `{% if docker %}` and `{% if web_framework == "flask" %}`
> work directly (the #782 fix) — no `features.*` namespace.

The demo exercises all three variable types:

- `type: string` — a plain text variable (`project_name`).
- `type: boolean` — a single y/N toggle (`docker`, `docker_compose`).
- `type: choice` — a numbered multi-valued picker (`web_framework`).

## Template

The `templates/generate/webapp/` template defines:

- **String variable:** `project_name`
- **Boolean `docker`** (default: `true`) — when on, prompts for
  `python_version` and renders `Dockerfile` + `.dockerignore`; when off,
  `extend.when: false` ignores those files.
- **Boolean `docker_compose`** (default: `true`, **`requires: [docker]`**) —
  renders `docker-compose.yml`; when off (or gated off because `docker` is
  off) its `extend.when: false` ignores the compose file.
- **Choice `web_framework`** (default: `none`) — picks between
  None / Flask / FastAPI. Each branch's `extend.when: <value>` controls
  `requirements.txt` + `wsgi.py` rendering and a silent `framework_version`
  variable.

## Usage

Run from this directory:

```bash
# Generate with all defaults (docker=on, docker_compose=on, web_framework=none)
pdm run python myapp.py generate webapp /tmp/myproject --defaults

# Generate interactively (prompts for each typed variable)
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

    -   name: docker
        type: boolean
        default: true
        extend:
            -   when: true
                variables:
                    -   name: python_version
                        prompt: "Python Version (for Docker)"
                        default: "3.13"
            -   when: false
                ignore:
                    - '.*Dockerfile.*'
                    - '.*\.dockerignore.*'

    -   name: docker_compose
        type: boolean
        default: true
        requires:
            - docker
        extend:
            -   when: false
                ignore:
                    - '.*docker-compose.*'

    -   name: web_framework
        type: choice
        prompt: "Web Framework"
        default: "none"
        options:
            -   value: "none"
                prompt: "None — no web framework"
            -   value: "flask"
                prompt: "Flask Web Framework"
            -   value: "fastapi"
                prompt: "FastAPI Web Framework"
        extend:
            -   when: "none"
                ignore:
                    - '.*requirements\.txt.*'
                    - '.*wsgi\.py.*'
            -   when: "flask"
                variables:
                    -   name: framework_version
                        prompt: false
                        default: "3.0"
                ignore:
                    - '.*fastapi.*'
            -   when: "fastapi"
                variables:
                    -   name: framework_version
                        prompt: false
                        default: "0.115"
                ignore:
                    - '.*flask.*'
```

## Typed Variables

### `type: string`

The released default. A plain `{name, prompt, default}` variable with optional
`case:` / `validate:`. Omitting `type:` is equivalent to `type: string`.

### `type: boolean`

A single y/N prompt rendered as `<prompt> [(Y)es/(N)o] [<default>]:` — e.g.
`Enable docker [(Y)es/(N)o] [Y]:`. With no `prompt:` key the label defaults to
`Enable <name>`; an explicit `prompt:` overrides it. Input `y`/`yes` → `True`,
`n`/`no` → `False`, empty → `default`. The resolved value is a real Python
`bool`, so it lands at the **top level** of the context. Use it in a
conditional:

```jinja
{% if docker %}...Dockerfile-only content...{% endif %}
```

For full control of the wording and accepted tokens, give `prompt:` an object
instead of a string — the author owns the text, and `accept:` / `reject:` are
case-insensitive token lists that map the answer to a `bool` (input matching
neither aborts, like a failed `validate:`):

```yaml
    -   name: docker
        type: boolean
        default: true
        prompt:
            text: "Use Docker? [(Y)ay/(N)ay]"
            accept: [y, yay]
            reject: [n, nay]
```

> Quote bool-like tokens (`"yes"`, `"no"`, `"on"`, `"off"`) inside
> `accept:` / `reject:` — under YAML 1.1 they otherwise decode to a Python
> `bool` and the loader rejects them with a clear error.

> **`{{ bool }}` interpolation gotcha:** a boolean rendered as *text*
> (`{{ docker }}`) interpolates the **capitalized Python repr** — `True` or
> `False` — **not** `true`/`false` and **not** `yes`/`no`. This is true for
> both the jinja2 and mustache (pystache) template handlers. Conditionals
> (`{% if docker %}`, mustache `{{#docker}}` / `{{^docker}}`) are the intended
> use and behave correctly; only direct text interpolation of a bool shows the
> `True`/`False` repr.

### `type: choice`

A numbered multi-valued picker. Under the hood it delegates to
`cement.utils.shell.Prompt` with `numbered=True`:

```
Web Framework

1: None — no web framework
2: Flask Web Framework
3: FastAPI Web Framework

Enter the number for your selection:
```

Choice schema keys:

- `options` — list of branches. Each branch is either a bare scalar
  (`options: ["1", "2"]`) or an object with `value:` (required, the resolved
  string `{{ web_framework }}` substitutes) and an optional `prompt:` label
  shown in the numbered list (falls back to `str(value)`).
- `default` — REQUIRED; must equal one of the option values (validated at
  config-load). Used as the Prompt's default-on-Enter and the `--defaults`
  headless value.
- The resolved choice value lands at the top level, so
  `{% if web_framework == "flask" %}` works directly.

## `extend:` — conditional effects

Each variable may carry an `extend:` list. A rule fires when its `when:`
matches the resolved value:

- **scalar equality:** `when: true` / `when: "flask"`
- **in-list membership:** `when: ["flask", "fastapi"]`
- **string regex** (string vars only): `when: "^3\\."`

A firing rule contributes its `variables:` (prompted *in place*, in
declaration order — including silent `prompt: false` metadata like
`framework_version`), `ignore:` (regex paths skipped), and `exclude:`
(paths copied verbatim, no rendering). Multiple matching rules compose.

## `requires:` — variable gating

A variable may declare `requires:` on other top-level variables:

- `requires: [docker]` — list of bare names; each must be truthy.
- `requires: {web_framework: flask}` — map form; equality.
- `requires: {web_framework: [flask, fastapi]}` — map form; in-list.

`requires:` resolves **top-level** variables only (nested `extend.variables`
are not addressable by name). The map form reuses the same matcher as
`extend.when`, so a string-typed prerequisite also accepts a regex.

Multiple entries are AND-ed and resolved order-independently. If a `requires:`
gate fails, the variable is set to its (typed) **default** at the top level
(so `{{ var }}` / `{% if var %}` never errors) and **none** of its `extend:`
rules fire. In this demo, disabling `docker` automatically gates off
`docker_compose` (which `requires: [docker]`), so `docker-compose.yml` is not
rendered.

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

`web_framework=none` ignores `requirements.txt` and `wsgi.py`, so they do not
appear in the rendered tree.

**With docker off** (`docker_compose` is auto-gated via `requires: [docker]`):

```text
/tmp/myproject/
├── README.md
└── app.py
```

No Dockerfile, no docker-compose.yml — gating off `docker` cascades to
`docker_compose`.

**With web_framework=fastapi** (other variables default):

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

[779]: https://github.com/datafolklabs/cement/issues/779
[782]: https://github.com/datafolklabs/cement/issues/782
