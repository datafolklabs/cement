# {{ description }}

## System Requirements

- Python 3.10 or newer
- (Optional) Docker, for container builds via the included `Dockerfile`

## Installation

```
$ pip install .
```

Or, from a built distribution / PyPI release:

```
$ pip install {{ label }}
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

Additional development requirements:

- [PDM](https://pdm-project.org/) (Python Dependency Manager) for build, dependency, and virtualenv management

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### install dependencies (creates a virtualenv automatically)

$ make setup


### run {{ label }} cli application

$ pdm run {{ label }} --help


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

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `{{ name }}`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it {{ label }} --help
```
