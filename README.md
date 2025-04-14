# Cement Framework

[![Built on Cement™](https://img.shields.io/badge/Built%20on%20Cement%E2%84%A2-3.0-yellow)](https://builtoncement.com)
[![PyPi Downloads](https://img.shields.io/pypi/dm/cement)](https://pypistats.org/packages/cement)
[![Continuous Integration Status](https://app.travis-ci.com/datafolklabs/cement.svg?branch=master)](https://app.travis-ci.com/github/datafolklabs/cement/)


Cement is an advanced Application Framework for Python, with a primary focus on Command Line Interfaces (CLI).  Its goal is to introduce a standard and feature-full platform for both simple and complex command line applications as well as support rapid development needs without sacrificing quality.  Cement is flexible, and its use cases span from the simplicity of a micro-framework to the complexity of a mega-framework. Whether it's a single file script or a multi-tier application, Cement is the foundation you've been looking for.

The first commit to Git was on Dec 4, 2009.  Since then, the framework has seen several iterations in design and has continued to grow and improve since its inception.  Cement is the most stable and complete framework for command line and backend application development.

## Installation

```
pip install cement
```

Optional CLI Extras (for development):

```
pip install cement[cli]
```


## Core Features

Cement core features include (but are not limited to):

- Core pieces of the framework are customizable via handlers/interfaces
- Handler system connects implementation classes with Interfaces
- Extension handler interface to easily extend framework functionality
- Config handler supports parsing multiple config files into one config
- Argument handler parses command line arguments and merges with config
- Log handler supports console and file logging
- Plugin handler provides an interface to easily extend your application
- Output handler interface renders return dictionaries to console
- Cache handler interface adds caching support for improved performance
- Controller handler supports sub-commands, and nested controllers
- Hook support adds a bit of magic to apps and also ties into framework
- Zero external dependencies* (not including optional extensions)
- 100% test coverage (`pytest`, `coverage`)
- 100% PEP8 compliance (`ruff`)
- Type annotation compliance (`mypy`)
- Extensive API Reference (`sphinx`)
- Tested on Python 3.8+


## Optional Extensions

Some extensions that are shipped with the mainline Cement source do require external dependencies.  It is the responsibility of the application developer to include these dependencies along with their application, as Cement explicitly does not include them. Dependencies can be installed via each extensions optional package (ex: `cement[colorlog]`, `cement[redis]`, etc).

See: [https://docs.builtoncement.com/extensions](https://docs.builtoncement.com/extensions)


## More Information

- [Official Website / Developer Documentation](http://builtoncement.com/)
- [PyPi Packages](http://pypi.python.org/pypi/cement/)
- [Github Source Code / Issue Tracking](http://github.com/datafolklabs/cement/)
- [Travis CI](https://travis-ci.org/datafolklabs/cement/)
- [Slack Channel](https://join.slack.com/t/cementframework/shared_invite/enQtMzU0OTc5MDQ4NDA0LWMwMzZiOTczZjM4ZjFiZDE3MDk4MzA5ZmYxNmZjNTk4NzUwMzcyN2VlMDc5NzIxYjQ1NzlmNzgyNDFjMWJmMWY)


## License

The Cement CLI Application Framework is Open Source and is distributed under the BSD License (three clause).  Please see the LICENSE file included with this software.


## Development

### Docker

This project includes a Docker Compose configuration that sets up all required services, and dependencies for development and testing.  This is the recommended path for local development, and is the only fully supported option.

The following creates all required docker containers, and launches an BASH shell within the `cement` dev container for development.
```
$ make dev

|> cement <| src #
```

The above is the equivalent of running:

```
$ docker compose up -d

$ docker compose exec cement /bin/bash
```

All execution is done *inside the docker containers*.


**Testing Alternative Versions of Python**

The latest stable version of Python 3 is the default, and target version accessible as the `cement` container within Docker Compose.  For testing against alternative versions of python, additional containers are created (ex: `cement-py38`, `cement-py39`, etc). You can access these containers via:

```
$ docker-compose ps
        Name                      Command               State     Ports
-------------------------------------------------------------------------
cement_cement-py38_1    /bin/bash                        Up
cement_cement-py39_1    /bin/bash                        Up
cement_cement-py310_1   /bin/bash                        Up
cement_cement-py311_1   /bin/bash                        Up
cement_cement-py312_1   /bin/bash                        Up
cement_cement_1         /bin/bash                        Up
cement_memcached_1      docker-entrypoint.sh memcached   Up       11211/tcp
cement_redis_1          docker-entrypoint.sh redis ...   Up       6379/tcp


$ docker-compose exec cement-py39 /bin/bash

|> cement-py39 <| src #
```


### Windows Targeted Development

*Windows development and support is not 100% complete.  Applications Built on Cement is known to run and work on Windows well, however it is not a primary target for development and as such the setup is not as streamlined and currently has several known issues.*

If you are developing on Windows, the recommended path is still Docker. However if you are specifically targeting development *for* Windows you will want to run Python/Cement natively which will require setting up a development environment on the Windows host. 

This is very rough (future doc coming), however the following will be required:

- Python 3.x (latest stable preferred)
  - pip
  - pipx
  - pdm
- Visual C++ 14.0 or Greater Build Tools
  - Including: CMake

Assuming Python/PIP are installed, the following will install PDM:

```
pip install pipx

pipx install pdm
```

C++ Build Tools are install, the following will create a development virtual env:

```
pdm venv create

pdm install --without memcached
```

You can then run the core tests:

```
pdm run pytest --cov=cement.core tests/core
```

*Note that only the core library is fully tested on Windows.*

Please explore the Makefile for helpers that may or may not work. Example, the following will run the same as the above `pdm run pytest` command:

```
make test-core
```

And, you can run Cement CLI via:

```
pdm run cement --help
```


### macOS Targeted Development

Similar to the above... if you are developing on macOS, the recommended path is still Docker. However if you are specifically targeting development *for* macOS you will want to run Python/Cement natively which will require setting up a development environment on the macOS host. 

This is less nuanced than Windows, however still required some dependencies that will not be fully covered here (example: memcached). The following will get you setup to run the core library tests.

```
pip install pipx

pipx install pdm

pdm venv create

pdm install --without memcached

make test-core
```

And, you can run Cement CLI via:

```
pdm run cement --help
```

### Running Tests and Compliance

Cement has a strict policy that all code and tests meet PEP8 guidelines, therefore `ruff` is called before any unit tests run.  All code submissions require 100% test coverage and PEP8 compliance:

Execute the following to run all compliance and unit tests:

```
$ make test
```

A coverage report is printed to console, as well as the HTML version created in `coverage-report`:

```
$ open coverage-report/index.html
```

See `Makefile` for all other common development actions.
