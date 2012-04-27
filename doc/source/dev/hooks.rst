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

    * :ref:`Cement Hook Module <cement2.core.hook>`
    
Defining a Hook
---------------

A hook can be defined as follows:

.. code-block:: python

    from cement2.core import foundation, hook
    
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

    from cement2.core import foundation, hook
    
    # First create the application
    app = foundation.CementApp('myapp')
    
    # Then define any application hooks
    hook.define('my_example_hook')

    # Register any hook functions.  In the real world, this would likely be
    # done elsewhere in the application such as in plugins.
    @hook.register()
    def my_example_hook():
        # do something
        something = "The result of my hook."
        return something
    
    @hook.register(name='my_example_hook')
    def my_function_with_some_other_name():
        # do something
        pass
        
    # Setup the application
    app.setup()
    
    
    
The @hook.register() decorator uses the name of the function you are 
decorating to determine the hook you are registering for, or you can pass the
name parameter.  Note that if combining with other decorators you must pass
the name parameter.

What you return depends on what the developer defining the hook is expecting.
Each hook is different, and the nature of the hook determines whether you need
to return anything or not.  That is up to the developer.  Also, the args and
kwargs coming in depend on the developer.  You have to be familiar with 
the purpose of the defined hook in order to know whether you are receiving any
args or kwargs.

Registering a hook just puts the function into the hook list.  This will be an
unbound function, so if you register a function that is a class method keep in
mind that 'self' doesn't exist in the context of when the hook is run.  For the
most part, standard unbound functions are best for hooks rather than controller
or other class methods.


Running a hook
--------------

Now that a hook is defined, and functions have been registered to that hook
all that is left is to run it.  Keep in mind, you don't want to run a hook
until after the application load process... meaning, after all plugins and 
other code are loaded.  If you receive an error that the hook doesn't exist,
then you are trying to register a hook to soon before the hook is defined.

.. code-block:: python

    from cement2.core import hook
    
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

    from cement2.core import backend, foundation, controller, handler, hook

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
    hook.define('myapp_default_command_hook')

    # register some hook functions

    @hook.register(name='myapp_default_command_hook', weight=0)
    def hook1(app):
        print 'Inside hook1 of %s.' % app.name
    
    @hook.register(name='myapp_default_command_hook', weight=100)
    def hook2(app):
        print 'Inside hook2 of %s.' % app.name

    @hook.register(name='myapp_default_command_hook', weight=-99)
    def hook3(app):
        print 'Inside hook3 of %s.' % app.name
    
    
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
    Inside hook3 of myapp.
    Inside hook1 of myapp.
    Inside hook2 of myapp.
    
    
As you can see, it doesn’t matter what order we register the hook, the 
weight runs then in order from lowest to highest.  

Cement Framework Hooks
----------------------

Cement has a number of hooks that tie into the framework.

cement_pre_setup_hook
^^^^^^^^^^^^^^^^^^^^^
        
Run first when CementApp.setup() is called.  The application object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_pre_setup_hook')
    def my_setup_hook(app):
        # do something before application setup()
        pass

cement_post_setup_hook
^^^^^^^^^^^^^^^^^^^^^^
        
Run last when CementApp.setup() is called.  The application object object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_post_setup_hook')
    def my_setup_hook(app):
        app.args.add_argument('-f', '--foo', dest='foo', action='store_true')
        

NOTE: This hook deprecated the cement_add_args_hook in version 1.9.2.

cement_pre_run_hook
^^^^^^^^^^^^^^^^^^^
        
Run first when CementApp.run() is called.  The application object object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_pre_run_hook')
    def my_pre_run_hook(app):
        # do something before application run()
        if not app.config.has_key('base', 'foo'):
            raise MyAppConfigError, "Required configuration 'foo' missing."

Note: This hook deprecated the cement_validate_config_hook in version 1.9.2.

cement_post_run_hook
^^^^^^^^^^^^^^^^^^^^
        
Run last when CementApp.run() is called.  The application object object is
passed as an argument.  Nothing is expected in return.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_post_run_hook')
    def my_post_run_hook(app):
        # Do something after application run() is called.
        return

cement_pre_render_hook
^^^^^^^^^^^^^^^^^^^^^^

Run first when CementApp.render() is called.  The application object, and
data dictionary are passed as arguments.  Must return either the original
data dictionary, or a modified one.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_pre_render_hook')
    def my_pre_render_hook(app, data):
        # Do something with data.
        return data
        
Note: This does not affect anything that is 'printed' to console.

cement_post_render_hook
^^^^^^^^^^^^^^^^^^^^^^^

Run last when CementApp.render() is called.  The application object, and 
rendered output text are passed as arguments.  Must return either the original
output text, or a modified version.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_post_render_hook')
    def my_post_render_hook(app, output_text):
        # Do something with output_text.
        return output_text

cement_on_close_hook
^^^^^^^^^^^^^^^^^^^^

Run when app.close() is called.  This hook should be used by plugins and 
extensions to do any 'cleanup' at the end of program execution.  Nothing is
expected in return.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_on_close_hook')
    def my_cleanup_hook(app):
        # Do something when the application close() is called.
        return
        
cement_signal_hook
^^^^^^^^^^^^^^^^^^

Run when signal handling is enabled, and the defined signal handler callback
is executed.  This hook should be used by the application, plugins, and
extensions to perform any actions when a specific signal is caught.  Nothing
is expected in return.

.. code-block:: python

    from cement2.core import hook
    
    @hook.register(name='cement_signal_hook')
    def my_signal_hook(signum, frame):
        # do something with signum/frame
        return
        