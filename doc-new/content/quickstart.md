---
title: "Quick Start Overview"
weight: 2
---

# Quickstart Overview

[comment]: <> (--------------------------------------------------------------)

## The Application Object

> Using CementApp Directly

```python
from cement.core.foundation import CementApp

with CementApp('myapp') as app:
    app.run()
```

The core of your application starts with the `CementApp` object, which can
technically be used direcly (as in the example), however in practice you will
almost always sub-class `CementApp` in order to configure it for your needs.

Cement uses `MetaMixin` classes everywhere, which allows the framework to
define default functionality but also provides an easy mechanism for
developers to override and customize.

> Sub-classing CementApp / Overriding Metadata Options

```python
from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults

# define default application configuration settings
defaults = init_defaults('myapp')
defaults['myapp']['foo'] = 'bar'

class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        config_defaults = defaults

with MyApp() as app:
    app.run()
    print("Foo => %s" % app.config.get('myapp', 'foo'))
```

> Usage

```
$ python myapp.py
Foo => bar
```

[comment]: <> (--------------------------------------------------------------)

## Configuration

> myapp.py

```python
from cement import App, init_defaults

defaults = init_defaults('myapp')
defaults['myapp']['foo'] = 'bar'

class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = defaults

with MyApp() as app:
    app.run()
    print("Foo => %s" % app.config.get('myapp', 'foo'))
```

> ~/.myapp.conf

```
[myapp]
foo = not-bar
```

> Usage

```
$ python myapp.py
Foo => not-bar
```


Cement applications support loading multiple configuration files 
out-of-the-box.  Configurations loaded from files are merged in to override
the applications default configuration settings.

By default, applications look for configuration files in the most common
places such as:

- `/etc/myapp/myapp.conf`
- `~/.myapp.conf`
- `~/.myapp/config`
- etc 

<aside class="info">
The list of configuration file paths can be customized via the meta option
CementApp.Meta.config_files.
</aside>

The builtin configuration handler is based on `ConfigParser` from the standard
library, and uses common unix-like config files where `blocks` or `sections`
are defined with `[brackets]`.  Additional support for the following file 
formats is provided via optional extensions:

 * Json
 * Yaml

<aside class="info">
ConfigHandler's provide dropin replacements for the default
ConfigParserConfigHandler, and are often based on it.  For example, the
JsonConfigHandler and YamlConfigHandler extensions do nothing more than
support reading alternative file formats.  Accessing the config settings in
the app is exactly the same
</aside>

[comment]: <> (--------------------------------------------------------------)

## Arguments

### Simple Argument Definitions

> myapp.py

```python

from cement import App

with App('myapp') as app:
    app.args.add_argument('-f', '--foo', 
                          help='notorous foo option', 
                          dest='foo')
    app.run()

    # do something with parsed arguments
    if app.pargs.foo is not None:
        print("Foo Argument => %s" % app.pargs.foo)

```

> Usage

```
$ python myapp.py --help
usage: myapp [-h] [--debug] [--quiet] [-f FOO]

optional arguments:
  -h, --help         show this help message and exit
  --debug            toggle debug output
  --quiet            suppress all output
  -f FOO, --foo FOO  notorous foo option

$ python myapp.py -f bar
Foo Argument => bar
```

Argument parsing is handled by `Argparse`, with the same usage that you're
familiar with.  That said, the power of the framework comes into play when 
we start talking about application controllers that streamline the process of 
mapping arguments and sub-commands to actions/functions (more on that later).


### Defining Arguments via Controllers

> myapp.py

```python

from cement.core.foundation import CementApp
from cement.ext.ext_argparse import ArgparseController, expose

class BaseController(ArgparseController):
    class Meta:
        label = 'base'

        # arguments are a list of tuples in the format `( [], dict() )`
        # as in `*args` and `**kwargs` that are passed to argparse
        arguments = [
            ( ['-f', '--foo'],
              dict(help='notorious foo option',
                   dest='foo') ),
        ]

    @expose()
    def default(self):
        print('Inside BaseController.default()')

        # do something with parsed arguments
        if self.app.pargs.foo is not None:
            print("Foo Argument => %s" % self.app.pargs.foo)

class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        handlers = [BaseController]

with MyApp() as app:
    app.run()

```

[comment]: <> (--------------------------------------------------------------)

## Logging

FIX ME


[comment]: <> (--------------------------------------------------------------)

## Output

FIX ME


[comment]: <> (--------------------------------------------------------------)

## Controllers

FIX ME


[comment]: <> (--------------------------------------------------------------)

## Framework Extensions

FIX ME


[comment]: <> (--------------------------------------------------------------)

## Application Plugins

FIX ME


[comment]: <> (--------------------------------------------------------------)

## Hooks

FIX ME
