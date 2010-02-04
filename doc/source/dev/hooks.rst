Hooks
=====

Hooks allow the developers to tie into different pieces of the application.
A hook can be defined anywhere, be it internally in the application, or in a
plugin.  Once a hook is defined, functions can be registered to that hook so
that when the hook is called, all functions registered to that hook will be 
run.  By defining a hook, you are saying that you are going to honor that hook
somewhere in your application.  Using descriptive hook names are good for
clarity.  For example, 'pre_database_connect_hook' is obviously a hook that
will be run before a database connection is attempted.

Cement has a number of hooks that tie into the Cement Framework:

Hook definitions:

    options_hook
        Used to add options to a namespaces options object

    post_options_hook
        Run after all options have been setup and merged

    validate_config_hook
        Run after config options are setup

    pre_plugins_hook
        Run just before all plugins are loaded (run once)

    post_plugins_hook
        Run just after all plugins are loaded (run once)
    
Defining a Hook
---------------

A hook can be define as follows:

.. code-block:: python

    from cement.core.hook import define_hook
    
    define_hook('my_example_hook')


It is a good idea to register hooks early on in the application loading 
process.  For plugins, you should define hooks in the '__init__' function
of your plugin class so it is registered first thing, before any other plugins
have a chance to register a function to that hook.

.. code-block:: python

    from cement.core.hook import define_hook
    from cement.core.plugin import CementPlugin, register_plugin
    
    @register_plugin() 
    class ExamplePlugin(CementPlugin):
        def __init__(self):
            define_hook('my_example_hook')
            CementPlugin.__init__(self,
                label='example',
                version=VERSION,
                description='Example plugin for helloworld',
                required_api=REQUIRED_CEMENT_API,
                banner=BANNER,
                controller = 'ExampleController', 
                )
            

If not registering a plugin, you could also define a hook in a controllers
'__init__' function.

.. code-block:: python

    from cement.core.controller import CementController, expose
    from cement.core.hook import define_hook
    
    class MyController(CementController):
        def __init__(self):
            CementController.__init__(self)
            define_hook('my_example_hook')
        
        @expose()
        def some_function(self, cli_opts, cli_args):
            pass
            

Registering Functions to a Hook
-------------------------------

A hook is just an identifier, but the functions registered to that hook are 
what get run when the hook is called.  Registering a hook should also be done
early in the application load process, however because it utilizes a 
decorator putting it toward the top of any controller file, or after 
plugin registration in your plugin file should be sufficient.  The following
is how to register a hook from a controller file:

.. code-block:: python

    from cement.core.controller import CementController, expose
    from cement.core.hook import register_hook
    
    @register_hook()
    def my_example_hook(self, *args, **kwargs):
        # do something
        something = "The result of my hook."
        return something
    
    
What you return depends on what the developer defining the hook is expecting.
Each hook is different, and the nature of the hook determines whether you need
to return anything or not.  That is up to the developer.  Also, the args and
kwargs coming in depend on the developer.  You have to be familiar with 
the purpose of the defined hook in order to know whether you are receiving any
args or kwargs.

Registering a hook just puts the function into the namespace.  This will be an
unbound function, so if you register a function that is a class method keep in
mind that 'self' doesn't exist in the context of when the hook is run.


Running a hook
--------------

Now that a hook is defined, and functions have been registered to that hook
all that is left is to run it.  Keep in mind, you don't want to run a hook
until after the application load process... meaning, after all plugins and 
controllers are loaded.  For the most part, you don't have much control over
this as that is all handled by Cement, however if you get an error that the
hook doesn't exist then you are probably running it too early.

.. code-block:: python

    from cement.core.hook import run_hooks
    
    for res in run_hooks('my_example_hook'):
        # do something with res
        pass
        
As you can see we iterate over the hook, rather than just calling 
'run_hooks()'.  This is necessary because run_hooks() yields the results from
each hook.  Hooks can be run anywhere *after* the hook is defined, and hooks
are registered to that hook.