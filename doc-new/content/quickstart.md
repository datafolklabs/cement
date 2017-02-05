---
weight: 2
title: Quick Start Overview
---

# Quick Start Overview

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

## Configuration Files

> myapp.py

```python
from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults

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

By default, applications look for configuration files in common places such as
`/etc/myapp/myapp.conf`, `~/.myapp.conf`, etc but can be customized via the
meta option `CementApp.Meta.config_files`.

The builtin configuration handler is based on `ConfigParser` from the standard
library, and uses common unix-like config files where `blocks` or `sections`
are defined with `[brackets]`.  Additional support for the following file 
formats is provided via optional extensions:

 * Json
 * Yaml


## Arguments

### Simple Argument Definitions

> myapp.py

```python

from cement.core.foundation import CementApp

with CementApp('myapp') as app:
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

## Logging
## Output
## Controllers
## Framework Extensions
## Plugins
## Hooks
## 

```python
# helloworld.py

from cement import App

with CementApp('helloworld') as app:
    app.run()
    print('Hello World!')
```

> USAGE


```
$ python helloworld.py
Hello World!
```

A simple `helloworld` application can be quick started with just a few lines
of code.


I can you saying, "Whoa whoa... hang on a minute.  This is a joke
right, all you did was print to STDOUT.  What kind of framework
is that?".  Well obviously this is just an introduction to show that the
creation of an application is dead simple.  Lets take a look further:

```
$ python helloworld.py --help
usage: helloworld [-h] [--debug] [--quiet]

optional arguments:
  -h, --help  show this help message and exit
  --debug     toggle debug output
  --quiet     suppress all output
```


As you can see, Argparse is already setup with a few options I see.  What 
else?

```
# enable framework logging (disabled by default)
$ export CEMENT_FRAMEWORK_LOGGING=1
    
# run with builtin debugging argument
$ python helloworld.py --debug
2017-02-04 17:36:09,169 (DEBUG) cement.core.foundation : laying cement for the 'helloworld' application
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'pre_setup'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'post_setup'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'pre_run'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'post_run'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'pre_argument_parsing'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'post_argument_parsing'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'pre_close'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'post_close'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'signal'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'pre_render'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : defining hook 'post_render'
2017-02-04 17:36:09,170 (DEBUG) cement.core.hook : registering hook 'add_handler_override_options' from cement.core.foundation into hooks['post_setup']
2017-02-04 17:36:09,171 (DEBUG) cement.core.hook : registering hook 'handler_override' from cement.core.foundation into hooks['post_argument_parsing']
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'extension' (IExtension)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'log' (ILog)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'config' (IConfig)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'mail' (IMail)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'plugin' (IPlugin)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'output' (IOutput)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'argument' (IArgument)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'controller' (IController)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : defining handler type 'cache' (ICache)
2017-02-04 17:36:09,171 (DEBUG) cement.core.handler : registering handler '<class 'cement.core.extension.CementExtensionHandler'>' into handlers['extension']['cement']
2017-02-04 17:36:09,171 (DEBUG) cement.core.foundation : now setting up the 'helloworld' application
2017-02-04 17:36:09,172 (DEBUG) cement.core.foundation : setting up helloworld.extension handler
2017-02-04 17:36:09,172 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_dummy' framework extension
2017-02-04 17:36:09,173 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_dummy.DummyOutputHandler'>' into handlers['output']['dummy']
2017-02-04 17:36:09,173 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_dummy.DummyMailHandler'>' into handlers['mail']['dummy']
2017-02-04 17:36:09,173 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_smtp' framework extension
2017-02-04 17:36:09,216 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_smtp.SMTPMailHandler'>' into handlers['mail']['smtp']
2017-02-04 17:36:09,217 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_plugin' framework extension
2017-02-04 17:36:09,219 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_plugin.CementPluginHandler'>' into handlers['plugin']['cement']
2017-02-04 17:36:09,219 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_configparser' framework extension
2017-02-04 17:36:09,223 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_configparser.ConfigParserConfigHandler'>' into handlers['config']['configparser']
2017-02-04 17:36:09,224 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_logging' framework extension
2017-02-04 17:36:09,224 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_logging.LoggingLogHandler'>' into handlers['log']['logging']
2017-02-04 17:36:09,224 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_argparse' framework extension
2017-02-04 17:36:09,226 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_argparse.ArgparseArgumentHandler'>' into handlers['argument']['argparse']
2017-02-04 17:36:09,227 (DEBUG) cement.core.foundation : adding signal handler <function cement_signal_handler at 0x10767bc80> for signal Signals.SIGTERM
2017-02-04 17:36:09,227 (DEBUG) cement.core.foundation : adding signal handler <function cement_signal_handler at 0x10767bc80> for signal Signals.SIGINT
2017-02-04 17:36:09,227 (DEBUG) cement.core.foundation : adding signal handler <function cement_signal_handler at 0x10767bc80> for signal Signals.SIGHUP
2017-02-04 17:36:09,227 (DEBUG) cement.core.foundation : setting up helloworld.config handler
2017-02-04 17:36:09,227 (DEBUG) cement.core.config : config file '/etc/helloworld/helloworld.conf' does not exist, skipping...
2017-02-04 17:36:09,227 (DEBUG) cement.core.config : config file '/Users/derks/.helloworld.conf' does not exist, skipping...
2017-02-04 17:36:09,227 (DEBUG) cement.core.config : config file '/Users/derks/.helloworld/config' does not exist, skipping...
2017-02-04 17:36:09,228 (DEBUG) cement.core.foundation : setting up helloworld.mail handler
2017-02-04 17:36:09,228 (DEBUG) cement.core.handler : merging config defaults from '<cement.ext.ext_dummy.DummyMailHandler object at 0x1078104e0>' into section 'mail.dummy'
2017-02-04 17:36:09,228 (DEBUG) cement.core.foundation : no cache handler defined, skipping.
2017-02-04 17:36:09,228 (DEBUG) cement.core.foundation : setting up helloworld.log handler
2017-02-04 17:36:09,228 (DEBUG) cement.core.handler : merging config defaults from '<cement.ext.ext_logging.LoggingLogHandler object at 0x107810240>' into section 'log.logging'
2017-02-04 17:36:09,228 (DEBUG) cement.ext.ext_logging : logging initialized for 'helloworld' using LoggingLogHandler
2017-02-04 17:36:09,228 (DEBUG) cement.core.foundation : setting up helloworld.plugin handler
2017-02-04 17:36:09,229 (DEBUG) cement.ext.ext_plugin : plugin config dir /etc/helloworld/plugins.d does not exist.
2017-02-04 17:36:09,229 (DEBUG) cement.ext.ext_plugin : plugin config dir /Users/derks/.helloworld/plugins.d does not exist.
2017-02-04 17:36:09,229 (DEBUG) cement.core.foundation : setting up helloworld.arg handler
2017-02-04 17:36:09,229 (DEBUG) cement.core.foundation : setting up helloworld.output handler
2017-02-04 17:36:09,229 (DEBUG) cement.core.foundation : setting up application controllers
2017-02-04 17:36:09,230 (DEBUG) cement.core.hook : running hook 'post_setup' (<function add_handler_override_options at 0x107039620>) from cement.core.foundation
2017-02-04 17:36:09,230 (DEBUG) cement.core.foundation : running pre_run hook
2017-02-04 17:36:09,230 (DEBUG) cement.core.hook : running hook 'post_argument_parsing' (<function handler_override at 0x10767bbf8>) from cement.core.foundation
2017-02-04 17:36:09,230 (DEBUG) cement.core.foundation : running post_run hook
Hello World!
2017-02-04 17:36:09,230 (DEBUG) cement.core.foundation : closing the helloworld application
```

## Getting Warmer

A more advanced example showcases some of the default application features.  
Notice the creation of command line arguments, default config creation, and 
logging.


```python
# myapp.py

from cement import App, init_defaults

# define default configuration settings
config = init_defaults('myapp')
config['myapp']['debug'] = False
config['myapp']['some_param'] = 'some value'

# define any hook functions here
def my_cleanup_hook(app):
    pass

# define the application class
class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = config
        extensions = ['daemon', 'json']
        hooks = [
            ('pre_close', my_cleanup_hook),
        ]

with MyApp() as app:
    # add arguments to the parser
    app.args.add_argument('-f', '--foo', 
                          action='store', 
                          metavar='STR',
                          help='the notorious foo option')

    # log stuff
    app.log.debug("About to run myapp!")

    # run the application
    app.run()

    # continue with additional application logic (handle parsed args, etc)
    if app.pargs.foo:
        app.log.info("Received argument: foo => %s" % app.pargs.foo)
```

> USAGE

```
$ python myapp.py -h
usage: myapp [-h] [--debug] [--quiet] [-o {json}] [--daemon] [-f STR]

optional arguments:
  -h, --help         show this help message and exit
  --debug            toggle debug output
  --quiet            suppress all output
  -o {json}          output handler
  --daemon           daemonize the process
  -f STR, --foo STR  the notorious foo option

$ python myapp.py -f bar --debug
2017-02-04 17:48:03,787 (DEBUG) myapp : About to run myapp!
2017-02-04 17:48:03,788 (INFO) myapp : Received argument: foo => bar
```

