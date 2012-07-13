Framework and Application Hooks
===============================

Hooks allow the developers to tie into different pieces of the application.
A hook can be defined anywhere, be it internally in the application, or in a
plugin.  Once a hook is defined, functions can be registered to that hook so
that when the hook is called, all functions registered to that hook will be 
run.  By defining a hook, you are saying that you are going to honor that hook
somewhere in your application.  Using descriptive hook names are good for
clarity.  For example, 'pre_database_connect_hook' is obviously a hook that
will be run before a database connection is attempted.
    
The most important thing to remember when defining hooks for your application
is to properly document them.  Include whether anything is expected in return
or what, if any, arguments will be passed to the hook functions when called.

API Reference:

    * :ref:`Cement Hook Module <cement.core.hook>`
    
Defining a Hook
---------------

A hook can be defined as follows:

.. code-block:: python

    from cement.core import foundation, hook
    
    # First create the application
    app = foundation.CementApp('myapp')
    
    # Then define any application hooks
    hook.define('my_example_hook')

    # Setup the application
    app.setup()
    

Hooks should be defined as early on in the bootstrap process as possible,
after the CementApp() is instantiated, but before 'app.setup()' is called.


Registering Functions to a Hook
-------------------------------

A hook is just an identifier, but the functions registered to that hook are 
what get run when the hook is called.  Registering a hook function should also 
be done early on in the bootstrap process (before the hook is called 
obviously).  

.. code-block:: python

    from cement.core import foundation, hook
    
    # First create the application
    app = foundation.CementApp('myapp')
    
    # Then define any application hooks
    hook.define('my_example_hook')

    def my_func():
        # do something
        something = "The result of my hook."
        return something
    
    def my_other_func():
        # do something
        pass

    # Register any hook functions.  In the real world, this would likely be
    # done elsewhere in the application such as in plugins.
    hook.register('my_example_hook', my_func)
    hook.register('my_example_hook', my_other_func)
    
    # Setup the application
    app.setup()
    
        
What you return depends on what the developer defining the hook is expecting.
Each hook is different, and the nature of the hook determines whether you need
to return anything or not.  That is up to the developer.  Also, the args and
kwargs coming in depend on the developer.  You have to be familiar with 
the purpose of the defined hook in order to know whether you are receiving any
args or kwargs.

Running a hook
--------------

Now that a hook is defined, and functions have been registered to that hook
all that is left is to run it.  Keep in mind, you don't want to run a hook
until after the application load process... meaning, after all plugins and 
other code are loaded.  If you receive an error that the hook doesn't exist,
then you are trying to register a hook to soon before the hook is defined.

.. code-block:: python

    from cement.core import hook
    
    for res in hook.run('my_example_hook'):
        # do something with res?
        pass
        
As you can see we iterate over the hook, rather than just calling 
'hook.run()'.  This is necessary because hook.run() yields the results from
each hook.  Hooks can be run anywhere *after* the hook is defined, and hooks
are registered to that hook.


Controlling Hook Run Order
--------------------------

Sometimes you might have a very specific purpose in mind for a hook, and need
it to run before or after other functions in the same hook.  For that reason
there is an optional 'weight' parameter that can be passed when registering a
hook function.  

The following is an example application that defines, registers, and runs
a custom application hook:

.. code-block:: python

    from cement.core import backend, foundation, controller, handler, hook

    # define an application base controller
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            interface = controller.IController
            label = 'base'
            description = "My Application does amazing things!"

            config_defaults = {}
            arguments = []
        
        @controller.expose(hide=True, aliases=['run'])
        def default(self):
            for res in hook.run('myapp_default_command_hook', self.app):
                pass

    # create an application
    app = foundation.CementApp('myapp', base_controller=MyAppBaseController)

    # define a hook
    hook.define('my_hook')

    def func1(app):
        print 'Inside func1 of %s.' % app.name
    
    def func2(app):
        print 'Inside func2 of %s.' % app.name

    def func3(app):
        print 'Inside func3 of %s.' % app.name
    
    # register some hook functions
    hook.register('my_hook', func1, weight=0)
    hook.register('my_hook', func2, weight=100)
    hook.register('my_hook', func3, weight=-99)        
    
    try:
        # setup the application
        app.setup()
    
        # run the application
        app.run()

    finally:
        # close the application
        app.close()
    
And the result is:

.. code-block:: text

    $ python test.py
    Inside func3 of myapp.
    Inside func1 of myapp.
    Inside func2 of myapp.
    
    
As you can see, it doesn’t matter what order we register the hook, the 
weight runs then in order from lowest to highest.  

Cement Framework Hooks
----------------------

Cement has a number of hooks that tie into the framework.

pre_setup
^^^^^^^^^
        
Run first when CementApp.setup() is called.  The application object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app):
        # do something before application setup()
        pass
    
    hook.register('pre_setup', my_hook)

post_setup
^^^^^^^^^^
        
Run last when CementApp.setup() is called.  The application object object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app):
        app.args.add_argument('-f', '--foo', dest='foo', action='store_true')
        
    hook.register('post_setup', my_hook)

pre_run
^^^^^^^
        
Run first when CementApp.run() is called.  The application object object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app):
        # do something before application run()
        if not app.config.has_key('base', 'foo'):
            raise MyAppConfigError, "Required configuration 'foo' missing."

    hook.register('pre_run', my_hook)
    
post_run
^^^^^^^^
        
Run last when CementApp.run() is called.  The application object object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app):
        # Do something after application run() is called.
        return

    hook.register('post_run', my_hook)
    
pre_render
^^^^^^^^^^

Run first when CementApp.render() is called.  The application object, and
data dictionary are passed as arguments.  Must return either the original
data dictionary, or a modified one.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app, data):
        # Do something with data.
        return data
    
    hook.register('pre_render', my_hook)
    
Note: This does not affect anything that is 'printed' to console.

post_render
^^^^^^^^^^^

Run last when CementApp.render() is called.  The application object, and 
rendered output text are passed as arguments.  Must return either the original
output text, or a modified version.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app, output_text):
        # Do something with output_text.
        return output_text

    hook.register('post_render', my_hook)
    
pre_close
^^^^^^^^^

Run first when app.close() is called.  This hook should be used by plugins and 
extensions to do any 'cleanup' at the end of program execution.  Nothing is
expected in return.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app):
        # Do something before application close() is called.
        return
    
    hook.register('pre_close', my_hook)

Note: This hook deprecates the 'cement_on_close_hook' since Cement >= 1.9.9.

post_close
^^^^^^^^^^

Run last when app.close() is called.  Most use cases need pre_close(), 
however this hook is available should one need to do anything after all other
'close' operations.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(app):
        # Do something after application close() is called.
        return
    
    hook.register('post_close', my_hook)

signal
^^^^^^

Run when signal handling is enabled, and the defined signal handler callback
is executed.  This hook should be used by the application, plugins, and
extensions to perform any actions when a specific signal is caught.  Nothing
is expected in return.

.. code-block:: python

    from cement.core import hook
    
    def my_hook(signum, frame):
        # do something with signum/frame
        return
        
    hook.register('signal', my_hook)
