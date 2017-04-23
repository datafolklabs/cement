---
weight: 3
title: Hooks
---

# Hooks

Hooks allow developers to tie into different pieces of the application, and/or
the Cement Framework. A hook can be defined anywhere, be it internally in the
application, or in a plugin.  Once a hook is defined, functions can be
registered to that hook so that when the hook is called, all functions
registered to that hook will be executed.  By defining a hook, you are saying
that you are going to honor that hook somewhere in your application or plugin.
Using descriptive hook names is good for clarity.  For example, the name 
`pre_database_connect` is obviously a hook that will be run just before a
database connection is attempted.

The most important thing to remember when defining hooks is to properly
document them.  Include whether anything is expected in return
or what, if any, arguments will be passed to the hook functions when called.


## Defining Hooks

> Defining a Hook via App.Meta

```python

from cement import App


class MyApp(App):
    class Meta:
        label = 'myapp'
        define_hooks = [
            'my_example_hook',
        ]
```

> Defining a Hook via App.setup()

```python
class MyApp(App):
    # ...
    
    def setup(self):
        super()
        self.hook.define('my_example_hook')
```

A hook can be defined anywhere, however it is best-practice to define the hook 
as early as possible.  A hook definition simply gives a label to the hook, and
allows the developer (or third-party plugin developers) to register functions
to that hook.  It's label is arbitrary.


## Registering Hook Functions

> Registering Hook Functions via App.Meta

```python
from cement import App


def my_hook1(app):
    # do something with app
    pass


def my_hook2(app):
    # do something with app
    pass


class MyApp(App):
    class Meta:
        label = 'myapp'

        ### list of tuples: ( 'hook_label', <hook_function> )
        hooks = [
            ('post_argument_parsing', my_hook1),
            ('pre_close', my_hook2),
        ]
```

> Registering Hook Functions via App.setup()

```python
class MyApp(App):
    # ...

    def setup(self):
        super()

        ### register hook functions
        self.hook.register('post_argument_parsing', my_hook1)
        self.hook.register('pre_close', my_hook2)
```

A hook label is just an arbitrary identifier, but the functions registered to
that hook are what get run when the hook is called.  Registering a hook
function should also be done early on in the bootstrap process, any time after
the application has been created, after the hook is defined, and before the
hook is run.  Note that every hook is different, and therefore should be
clearly documented by the 'owner' of the hook (application developer, plugin
developer, etc).

What you return depends on what the developer defining the hook is expecting.
Each hook is different, and the nature of the hook determines whether you need
to return anything or not.  That is up to the developer.  Also, the `*args`
and `**kwargs` coming in depend on the developer.  You have to be familiar
with the purpose of the defined hook in order to know whether you are
receiving any `*args` or `**kwargs`.


## Running Hooks

> Running a Hook

```python
with MyApp() as app:
    app.run()

    for res in app.hook.run('my_example_hook'):
        # do something with res?
        pass
```


Now that a hook is defined, and functions have been registered to that hook,
all that is left is to run it.  As you can see in the example, we iterate over
the hook rather than just calling `app.hook.run()` by itself.  This is
necessary because `app.hook.run()` yields the results from each hook function
as they are run. Hooks can be run anywhere **after** the hook is defined, and
hooks are registered to that hook.

<aside class='warning'>
Keep in mind, you don't want to run a hook until after the application load
process... meaning, after all plugins and other code are loaded.  If you
receive an error that the hook doesn't exist, then you are trying to register
a hook too soon before the hook is defined. Likewise, if it doesn't seem like
your hook is running and you don't see it mentioned in `--debug` output, you
might be registering your hook **after** the hook has already run.
</aside>


## Controlling Hook Run Order

> Example: Hook Run Order

```python

from cement import App


### define hook functions

def func1(app):
    print('Inside hook func1')


def func2(app):
    print('Inside hook func2')


def func3(app):
    print('Inside hook func3')


class MyApp(App):
    class Meta:
        label = 'myapp'
        
        ### define my_hook
        define_hooks = [
            'my_hook',
        ]

        ### register functions to my_hook
        hooks = [
            ('my_hook', func1, weight=0),
            ('my_hook', func2, weight=100),
            ('my_hook', func3, weight=-99),
        ]

with MyApp() as app:
    app.run()

    ### execute my_hook
    for res in app.hook.run('my_hook', app)
        pass
```

> Usage

```bash
$ python myapp.py
Inside hook func3
Inside hook func1
Inside hook func2
```

Sometimes you might have a very specific purpose in mind for a hook, and need
it to run before or after other functions in the same hook.  For that reason
there is an optional `weight` parameter that can be passed when registering
a hook function.

As you can see in the example, it doesn’t matter what order we register the
hook, the weight runs then in order from lowest to highest.


## Cement Framework Hooks

> Example Usage of Framework Hooks

```python

from cement import App


### handle arguments before app.run() is called
def inspect_arguments(app):
    if app.pargs.foo is not None:
        print('Foo Argument Was Passed!')


class MyApp(App):
    class Meta:
        label = 'myapp'
        hooks = [
            ('post_argument_parsing', inspect_arguments),
        ]


with MyApp() as app:
    app.args.add_argument('--foo')
    app.run()
```

> Usage

```bash
$ python myapp.py --foo bar
Foo Argument Was Passed!
```

Cement has a number of hooks that tie into the framework.

### pre_setup

Run first when ``CementApp.setup()`` is called.  The application object is
passed as an argument.  Nothing is expected in return.


### post_setup

Run last when CementApp.setup() is called.  The application object is
passed as an argument.  Nothing is expected in return.


### pre_run

Run first when CementApp.run() is called.  The application object is
passed as an argument.  Nothing is expected in return.


### post_run

Run last when CementApp.run() is called.  The application object is
passed as an argument.  Nothing is expected in return.


### pre_argument_parsing

Run after CementApp.run() is called, just *before* argument parsing happens.
The application object is passed as an argument to these hook
functions.  Nothing is expected in return.


### post_argument_parsing

Run after CementApp.run() is called, just *after* argument parsing happens.
The application object is passed as an argument to these hook
functions.  Nothing is expected in return.

This hook is generally useful where the developer needs to perform actions
based on the arguments that were passed at command line, but before the
logic of `app.run()` happens.


### pre_render

Run first when CementApp.render() is called.  The application object, and
data dictionary are passed as arguments.  Must return either the original
data dictionary, or a modified one.

Note: This does not affect anything that is 'printed' to console.


### post_render

Run last when CementApp.render() is called.  The application object, and
rendered output text are passed as arguments.  Must return either the original
output text, or a modified version.


### pre_close

Run first when app.close() is called.  This hook should be used by plugins and
extensions to do any 'cleanup' at the end of program execution.  Nothing is
expected in return.


### post_close

Run last when app.close() is called.  Most use cases need pre_close(),
however this hook is available should one need to do anything after all other
'close' operations.


### signal

Run when signal handling is enabled, and the defined signal handler callback
is executed.  This hook should be used by the application, plugins, and
extensions to perform any actions when a specific signal is caught.  Nothing
is expected in return.