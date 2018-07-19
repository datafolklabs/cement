# {{ description }}

## Installation

```
$ pip install -r requirements.txt

$ pip install setup.py
```

## Development

### Environment Setup

This project includes a basic Docker Compose configuration that will setup a local development environment with all dependencies, and services required for development and testing.

```
$ make dev
[...]
|> {{ label }} <| app #
```

The `{{ label }}` command line application is installed in `develop` mode, therefore all changes will be live and can be tested immediately as code is modified.

```
|> {{ label }} <| app # {{ label }} --help
```

### Running Tests

Execute tests from within the development environment:

```
|> {{ label }} <| app # make test
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
usage: {{ label }} [-h] [--debug] [--quiet] [-o {json,yaml}] [-v] {command1} ...

{{ description }}

optional arguments:
  -h, --help      show this help message and exit
  --debug         toggle debug output
  --quiet         suppress all output
  -o {json,yaml}  output handler
  -v, --version   show program's version number and exit

sub-commands:
  {command1}
    command1      example sub command1

Usage: {{ title }} command1 --foo bar
```
