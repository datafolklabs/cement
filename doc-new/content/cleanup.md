---
weight: 4
title: Cleanup
---

# Application Cleanup

> Automatic Cleanup (Builtin)

```python
from cement import App

### both .setup() / .close() called automatically by `with`

with App('myapp') as app:
    app.run()


### the above is equivalent to

app = App('myapp')
app.setup()
app.run()
app.close()
```

The concept of 'cleanup' after application run time is nothing new.  What
happens during 'cleanup' all depends on the application.  This might mean
closing and deleting temporary files, removing session data, or deleting a PID
(Process ID) file.

To allow for application cleanup not only within your program, but also
external plugins and extensions, there is the `app.close()` function that
must be called after `app.run()` regardless of any exceptions or runtime
errors.  Note that `app.close()` is called automatically when using the
Python `with` operator, so it is not generally something you call directly,
but it is important to know how and when it is called.

Calling `app.close()` ensures that the ``pre_close`` and ``post_close``
framework hooks are run, allowing extensions/plugins/etc to cleanup after the
program runs.


## Exit Status and Error Codes

> Setting Exit Code on Application Close

```python

from cement import App


### set exit_on_close for production use

class MyApp(App):
    class Meta:
        label = 'myapp'
        exit_on_close = True


### disable it for testing

class MyAppForTesting(MyApp):
    class Meta:
        exit_on_close = False


with MyApp() as app:
    try:
        app.run()
    except Exception as e:
        ### set exit code to use on app.close()
        app.exit_code = 1

```


You can optionally set the status code that your application exists with via
`App.exit_code`, however you must also ensure that the meta option 
`App.Meta.exit_on_close` is enabled.

<aside class="warning">
Note that Cement will not call SystemExit unless App.Meta.exit_on_close is
enabled.  You will find that calling SystemExit in testing is very
problematic, therefore you will likely want to enable App.Meta.exit_on_close
for production, but not for testing.
</aside>

Note that the default exit code is `0`, and any *uncaught exceptions* will
cause the application to exit with a code of `1` (error).


## Running Cleanup Code

> Example: Running Cleanup Code Via Hooks

```python

import os
from tempfile import mkstemp
from cement import App, init_defaults

defaults = init_defaults('myapp')
defaults['myapp']['tmp_file'] = mkstemp()[1]


def my_cleanup_hook(app):
    # do something with app...
    
    tmp_file = app.config.get('myapp', 'tmp_file')
    if os.path.exists(tmp_file):
        app.log.warning('removing tmp file: %s' % tmp_file)
        os.remove(tmp_file)


class MyApp(App):
    class Meta:
        label = 'myapp'
        config_defaults = defaults
        hooks = [
            ('pre_close', my_cleanup_hook),
        ]


with MyApp() as app:
    app.run()

```

> Usage

```
$ python myapp.py
WARNING: removing tmp file: /tmp/tmpifmxsfid

```

Any extension, plugin, or even the application itself that has 'cleanup'
code should do so within the `pre_close` or `post_close` hooks to ensure
that it gets run.  See the `Hooks` section of the documentation for more
information on running framework hooks.
