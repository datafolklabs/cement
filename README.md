# Cement Framework

[![Built on Cement™](https://img.shields.io/badge/Built%20on%20Cement%E2%84%A2-3.0-yellow)](https://builtoncement.com)
[![PyPi Downloads](https://img.shields.io/pypi/dm/cement)](https://pypistats.org/packages/cement)
[![Continuous Integration Status](https://app.travis-ci.com/datafolklabs/cement.svg?branch=master)](https://app.travis-ci.com/github/datafolklabs/cement/)


Cement is an advanced Application Framework for Python, with a primary focus on Command Line Interfaces (CLI).  Its goal is to introduce a standard, and feature-full platform for both simple and complex command line applications as well as support rapid development needs without sacrificing quality.  Cement is flexible, and it's use cases span from the simplicity of a micro-framework to the complexity of a mega-framework. Whether it's a single file script, or a multi-tier application, Cement is the foundation you've been looking for.

The first commit to Git was on Dec 4, 2009.  Since then, the framework has seen several iterations in design, and has continued to grow and improve since it's inception.  Cement is the most stable, and complete framework for command line and backend application development.

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
- 100% test coverage (`pytest`)
- 100% PEP8 compliant (`flake8`)
- Extensive API Reference (`sphinx`)
- Tested on Python 3.8+

*Some optional extensions that are shipped with the mainline Cement sources do require external dependencies.  It is the responsibility of the application developer to include these dependencies along with their application, as Cement explicitly does not include them.*


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

This project includes a `docker-compose` configuration that sets up all required services, and dependencies for development and testing.  This is the recommended path for local development, and is the only fully supported option.

The following creates all required docker containers, and launches an BASH shell within the `cement` dev container for development.
```
$ make dev

|> cement <| src #
```

The above is the equivalent of running:

```
$ docker-compose up -d

$ docker-compose exec cement /bin/bash
```

**Testing Alternative Versions of Python**

The latest stable version of Python 3 is the default, and target version accessible as the `cement` container within Docker Compose.  For testing against alternative versions of python, additional containers are created (ex: `cement-py38`, `cement-py39`, etc). You can access these containers via:

```
$ docker-compose ps
        Name                      Command               State     Ports
-------------------------------------------------------------------------
cement_cement-py38_1   /bin/bash                        Up
cement_cement-py39_1   /bin/bash                        Up
cement_cement-py310_1   /bin/bash                        Up
cement_cement-py311_1   /bin/bash                        Up
cement_cement_1        /bin/bash                        Up
cement_memcached_1     docker-entrypoint.sh memcached   Up      11211/tcp
cement_redis_1         docker-entrypoint.sh redis ...   Up      6379/tcp


$ docker-compose exec cement-py39 /bin/bash

|> cement-py39 <| src #
```


### VirtualENV

An traditional VirtualENV helper is available:

```
$ make virtualenv

$ source env/bin/activate

|> cement <| $
```

### Vagrant

An alternative option is included to run Vagrant for development.  This is partially supported, primarily for the purpose of developing/testing on Windows as well as testing specific issues on target operating systems.

To see a list of configured systems:

```
$ vagrant status
```

#### Linux

```
$ vagrant up linux

$ vagrant ssh linux

vagrant@linux $ cd /vagrant

vagrant@linux $ bash scripts/vagrant/bootstrap.sh

vagrant@linux $ make virtualenv

vagrant@linux $ source env/bin/activate

|> cement >| $
```

#### Windows

*Windows development and support is not 100% complete.  Cement is known to run and work on Windows, however it is not a primary target for development and as such the setup is not as streamlined and currently has several known errors.*

The following assumes you're running these two initial commands from a unix based system:

```
$ make clean

$ vagrant up windows
```

RDP or Login to Desktop/Console, and open a PowerShell terminal:

```
C:\> cd C:\Vagrant

C:\Vagrant> powershell.exe scripts\vagrant\bootstrap.ps1

C:\Vagrant> make virtualenv-windows

C:\Vagrant> .\env-windows\Scripts\activate.ps1

C:\Vagrant> make test-core
```

*Note that only the core library is fully tested on Windows.*


### Running Tests and Compliance

Cement has a strict policy that all code and tests meet PEP8 guidelines, therefore `flake8` is called before any unit tests run.  All code submissions require 100% test coverage and PEP8 compliance:

Execute the following to run all compliance and unit tests:

```
$ make test
```

A coverage report is printed to console, as well as the HTML version created in `coverage-report`:

```
$ open coverage-report/index.html
```

See `Makefile` for all other common development actions.
