# Demo: Generate Extension - Features

Demonstrates the `features` support in the `generate` extension, which allows
`.generate.yml` templates to conditionally include/exclude files and prompt for
additional variables based on optional feature toggles.

## Template

The `templates/generate/webapp/` template defines:

- **Base variable:** `project_name`
- **Feature: `docker`** (default: enabled) — includes `Dockerfile` and
  `.dockerignore`, prompts for `python_version`
- **Feature: `docker_compose`** (default: enabled, **requires: docker**) —
  includes `docker-compose.yml`

## Usage

Run from this directory:

```bash
# Generate with all defaults (docker=on, docker_compose=on)
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
        default: true
        requires:
            - docker
        disabled:
            ignore:
                - '.*docker-compose.*'
```

## What to Expect

**With defaults** (both features enabled):

```text
/tmp/myproject/
├── .dockerignore
├── Dockerfile
├── README.md
├── app.py
└── docker-compose.yml
```

**With docker disabled** (docker_compose is auto-disabled via `requires`):

```text
/tmp/myproject/
├── README.md
└── app.py
```

No Dockerfile, no docker-compose.yml — disabling docker automatically
disables docker_compose because it requires docker.

**With docker enabled, docker_compose disabled**:

```text
/tmp/myproject/
├── .dockerignore
├── Dockerfile
├── README.md
└── app.py
```
