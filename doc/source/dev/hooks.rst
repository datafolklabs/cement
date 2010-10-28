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

    post_bootstrap_hook
        Run just after the root bootstrap is loaded.  Note that Plugins can
        not use this hook because it runs before plugins are loaded.  Use 
        post_plugins_hook instead.
        
    validate_config_hook
        Run after config options are setup

    pre_plugins_hook
        Run just before all plugins are loaded (run once)

    post_plugins_hook
        Run just after all plugins are loaded (run once)
        
    
Defining a Hook
---------------

A hook can be defined as follows:

.. code-block:: python

    from cement.core.hook import define_hook
    
    define_hook('my_example_hook')


Hooks are defined during the bootstrap process, and should be added to the 
bootstrap file for the namespace they relate to.

**./helloworld/bootstrap/example.py**:

.. code-block:: python

    from cement.core.hook import define_hook
    from cement.core.plugin import CementPlugin, register_plugin
    
    define_hook('my_example_hook')
    ...
            

Registering Functions to a Hook
-------------------------------

A hook is just an identifier, but the functions registered to that hook are 
what get run when the hook is called.  Registering a hook should also be done
during the bootstrap process The following is how to register a hook from a 
controller file:

**./helloworld/bootstrap/someothernamespace.py**:

.. code-block:: python

    from cement.core.hook import register_hook
    
    @register_hook()
    def my_example_hook(*args, **kwargs):
        # do something
        something = "The result of my hook."
        return something
    
    @register_hook(name='some_other_hook_name')
    def my_function(*args, **kw):
        # do something
    ...
    
    
The @register_hook() decorator uses the name of the function you are 
decorating to determine the hook you are registering for, or you can pass the
name parameter.  Note that if combining with other decorators you must pass
the name parameter.  It should also be noted, you probably don't want to 
decorate a command function [one that is @expose()'d] as a hook.

What you return depends on what the developer defining the hook is expecting.
Each hook is different, and the nature of the hook determines whether you need
to return anything or not.  That is up to the developer.  Also, the args and
kwargs coming in depend on the developer.  You have to be familiar with 
the purpose of the defined hook in order to know whether you are receiving any
args or kwargs, but either way you ant to accept them.

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


Controlling Hook Run Order
--------------------------

Sometimes you might have a very specific purpose in mind for a hook, and need
it to run before or after other functions in the same hook.  For that reason
there is an optional 'weight' option that can be passed when registering a
hook function.  

First I'm going to define the hook, and also create an example command here
that will run the hook.

**./helloworld/controllers/root.py**:

.. code-block:: python

    from cement.core.hook import define_hook, run_hooks
    from cement.core.controller import CementController, expose
    
    define_hook('my_example_hook')
    
    class RootController(CementController):
        @expose()
        def hook_example(self):
            for res in run_hooks('my_example_hook'):
                pass
                

Then, we need to register functions into that hook, which we will do from 
another controller:
                
**./helloworld/controllers/example.py**:

.. code-block:: python

    from cement.core.hook import register_hook
    
    @register_hook(weight=99)
    def my_example_hook(*args, **kwargs):
        print "In example_hook number 1, weight = 99"

    @register_hook(weight=-1000)
    def my_example_hook(*args, **kwargs):
        print "In example_hook number 2, weight = -1000"

    @register_hook()
    def my_example_hook(*args, **kwargs):
        print "In example_hook number 3, weight = 0 (defaullt)"

    # snipped the rest of the file


We probably wouldn’t register the same hook from the same place, but I wanted 
to in order to show how hooks are ordered by weight. 

Note, you must iterate over run_hooks as it yields the results of the 
function. And the result?

.. code-block:: text

    $ helloworld hook-example
    loading example plugin
    loading clibasic plugin
    In example_hook number 2, weight = -1000
    In example_hook number 3, weight = 0 (defaullt)
    In example_hook number 1, weight = 99


As you can see, it doesn’t matter what order we register the hook, the 
weight runs then in order from lowest to highest.  Hooks are awesome and 
provide a little bit of magic to your application.  Be sure to properly 
document any hooks you define, what their purpose is and where they will 
be run.

