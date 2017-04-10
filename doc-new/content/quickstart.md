---
title: "Quick Start Overview"
weight: 2
---

# Quickstart Overview

This section is intended to give a brief overview of some of the most commonly
used core features of Cement.  Please do not be discouraged if you don't
"get it" right away.  Please also do not think, "is this it?".  This is not
intended to be an exhaustive end-all-be-all coverage of every feature of the
framework.

Some assumptions are being made here.  Primarily, we assume that you've used
and are familiar with Python.  The quickstart is intended to give a high level
look at using Cement.  Please dive deeper into the individual sections after
the quickstart in order to gain a better understanding of each component.


[comment]: <> (--------------------------------------------------------------)

## The Application Object

> Using Cement App Directly

```python
from cement import App

with App('myapp') as app:
    app.run()
```

> Sub-classing Cement App

```python
from cement import App

class MyApp(App):
    class Meta:
        label = 'myapp'

with MyApp() as app:
    app.run()
```

> Usage

```bash
$ python myapp.py --help
usage: myapp [-h] [--debug] [--quiet]

optional arguments:
  -h, --help  show this help message and exit
  --debug     toggle debug output
  --quiet     suppress all output
```

The core of your application starts with the Cement `App` object, which we
will refer to throughout this documentation as:

 * `App` - The uninstantiated Cement `App` base class
 * `MyApp` - The uninstatiated/sub-classed Cement application you are creating
 * `app` - The instantiated application object


Technically, Cement `App` can be used direcly (as in the example), however in
practice you will almost always sub-class `App` in order to configure it for
your needs (I.e. `MyApp`).


[comment]: <> (--------------------------------------------------------------)

## MetaMixin's

> Sub-classing Cement App / Overriding Metadata Options

```python
from cement import App, init_defaults

# define default application configuration settings
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

> Usage

```
$ python myapp.py
Foo => bar
```

Cement uses `MetaMixin` classes everywhere, which allows the framework to
define default functionality but also provides an easy mechanism for
developers to override and customize.  

This is implemented by declaring a `Meta` class, under your application and/or
other Cement Handler classes.  All Meta-options can also be overridden by any
`**kwargs` that are passed to the parent class that is being instantiated. 

I.e. `App('myapp', config_defaults={'foo': 'bar'})`

Nearly every Cement class has an associated `Meta` class, which we often
refer to as `App.Meta`, `SomeHandlerClass.Meta`, etc.  The
instantiated object is refered to in code as `App._meta`,
`SomeHandlerClass._meta`, etc.


[comment]: <> (--------------------------------------------------------------)

## Interfaces and Handlers

> Overriding Default Framework Handlers

```python
from cement import App
from cement.ext.ext_configparser import ConfigParserConfigHandler


class MyConfigHandler(ConfigParserConfigHandler):
    class Meta:
        label = 'my_config_handler'

    # do something to subclass/re-implement 
    # config handler here...


class MyApp(App):
    class Meta:
        label = 'myapp'
        config_handler = 'my_config_handler'
        handlers = [
            MyConfigHandler
        ]
```


All aspects of the framework are broken up into interfaces, and handlers.
Interfaces define some functionality, and Handlers implement that
functionality. Cement defines the following interfaces:

- `extension` - Framework extensions loading
- `log` - Logging to console/file
- `config` - Application Configuration defaults, overrides by file, etc
- `mail` - Mail sending (smtp, etc)
- `plugin` - Application plugin loading
- `output` - Output rendering (JSON, Yaml, Mustache Templates, etc)
- `argument` - Command line argument parsing
- `controller` - Command dispatch (sub-commands, sub-command arguments, etc)
- `cache` - Key/Value data store (memcached, redis, etc)

For example, the builtin configuration handler
`ConfigParserConfigHandler`, implements the `config` interface.  Handlers
are referred to by the interfaces they implement, such as
`config.configparser`, `config.json`, `config.yaml`, etc.

<aside class="info">
    Application developers can also define their own interfaces, allowing
    customization by plugins.
</aside>

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


Cement supports loading multiple configuration files out-of-the-box.  
Configurations loaded from files are merged in, overriding the applications
default settings (`App.Meta.config_defaults`).

The default configuration handler is `ConfigParserConfigHandler`, based on
`ConfigParser` in the standard library, and is instantiated as
`app.config`.

Cement looks for configuration files in the most common places such as:

- `/etc/myapp/myapp.conf`
- `~/.myapp.conf`
- `~/.myapp/config`
- etc 

<aside class="info">
The list of configuration file paths can be customized via the meta option
App.Meta.config_files.
</aside>

The builtin configuration handler `ConfigParserConfigHandler` uses common
unix-like config files where `blocks` or `sections` are defined with
`[brackets]`.  Additional support for the following file formats is provided
via optional extensions:

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

> Simple Arguments Defined With Cement App

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

> Arguments Defined With Controllers

```python

from cement import App, Controller, ex


class Base(Controller):
    class Meta:
        label = 'base'

        arguments = [
            # list of tuples in the format `( [], {} )`
            ( [ '-f', '--foo' ],
              { 'help' : 'notorious foo option',
                'dest' : 'foo' } ),
        ]

    @ex(hide=True)
    def _default(self):
        print('Inside BaseController._default()')

        # do something with parsed arguments
        if self.app.pargs.foo is not None:
            print("Foo Argument => %s" % self.app.pargs.foo)


class MyApp(App):
    class Meta:
        label = 'myapp'
        handlers = [Base]


with MyApp() as app:
    app.run()

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
