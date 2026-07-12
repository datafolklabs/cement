# A Simple TODO Application

## Installation

```
$ pip install .
```

## Development

This project uses [pdm-backend](https://backend.pdm-project.org/) packaging: all
build, metadata, runtime, and dev dependencies live in `pyproject.toml` — the
legacy setuptools packaging files are gone. See the `todo-tutorial` walkthrough on
[builtoncement.com](https://builtoncement.com) for the full narrative.

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### install project + dev dependencies

$ make setup    # or: pdm install


### run todo cli application

$ todo --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile` (builds with `pdm build`):

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `My TODO Application`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it todo --help
```
