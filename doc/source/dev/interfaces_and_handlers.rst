.. _interfaces-and-handlers:

Interfaces and Handlers
=======================

Cement has a unique interface and handler system that is used to break up 
pieces of the framework and allow customization of how Cement handles 
everything from logging to config file parsing, and almost every action in 
between.

The Cement Interface code is loosely modeled after `Zope Interface <http://old.zope.org/Products/ZopeInterface>`_
which allows a developer to define an interface that other developers can then
create implementations for.  For example, an interface might define that a 
class have a function called 'setup()'.  Any implementation of that interface
must provide a function called 'setup()', and perform the expected actions
when called.

In Cement2, we call the implementation of interfaces 'handlers' and provide the 
ability to easily register, and retrieve them via the :ref:`cement2.core.handler`
library.

API References:

    * :ref:`Cement Interface Module <cement2.core.interface>`
    * :ref:`Cement Handler Module <cement2.core.handler>`
    
    
Defining an Interface
---------------------

Cement uses interfaces and handlers extensively to manage the framework, 
however developers can also make use of this system to provide a clean, and
standardized way of allowing other developers to customize their application.

The following defines a basic interface:

.. code-block:: python

    from cement2.core import interface, handler

    class MyInterface(interface.Interface):
        class imeta:
            label = 'myinterface'

        # Must be provided by the implementation
        meta = interface.Attribute('Handler meta-data')
        my_var = interface.Attribute('A variable of epic proportions.')
    
        def setup(config_obj):
            """
            The setup function is called during application initialization and
            must 'setup' the handler object making it ready for the framework
            or the application to make further calls to it.
        
            Required Arguments:
        
                config_obj
                    The application configuration object.  This is a config object 
                    that implements the IConfigHandler interface and not a config 
                    dictionary, though some config handler implementations may 
                    also function like a dict (i.e. configobj).
                
            Returns: n/a
        
            """

        def do_something():
            """
            This function does something.

            """

    handler.define(MyInterface)

The above simply defines the interface.  It does *not* implement any 
functionality, and should never been used directly.  This is why the class
functions do not have an argument of 'self', nor do they contain any code
other than comments.

That said, what is required is an 'imeta' class that is used to interact
with the interface.  At the very least, this must include a unique 'label'
to identify the interface.  This can also be considered the 'handler type'.  
For example, the ILog interface has a label of 'log'.

Notice that we defined 'meta' and 'my_var' as Interface Attributes.  This is
a simple identifier that describes an attribute that an implementation is 
expected to provide.

Validating Interfaces
---------------------

A validator call back function can be defined in the interfaces imeta class
like this:

.. code-block:: python

    from cement2.core import interface, handler

    def my_validator(klass, obj):
        members = [
            'setup',
            'do_something',
            'my_var',
            ]
        interface.validate(MyInterface, obj, members)

    class MyInterface(interface.Interface):
        class imeta:
            label = 'myinterface'
            validator = my_validator
        ...

When 'handler.register()' is called to register a handler to an interface,
the validator is called and the handler obj is passed to the validator.  In
the above example, we simply define what members we want to validate for and
then call interface.validate() which will raise 
cement2.core.exc.CementInterfaceError if validation fails.  It is not 
necessary to use interface.validate() but it is useful.  In general, the key
thing to note is that a validator either raises CementInterfaceError or does
nothing if validation passes.

Registering Handlers to an Interface
------------------------------------

An interface simply defines what an implementation is expected to provide, 
where a handler actually implements the interface.  The following example
is a handler that implements the MyInterface above:

.. code-block:: python

    from cement2.core import interface
    
    class MyHandler(object):
        class meta:
            interface = MyInterface
            label = 'my_handler'
            description = 'This handler implements MyInterface'
            defaults = {
                foo='bar'
                }
    
        my_var = 'This is my var'
        
        def __init__(self):
            self.config = None
            
        def setup(config_obj):
            self.config = config_obj
            
        def do_something(self):
            print "Doing work!"

    handler.register(MyHandler)

The above is a simple class that meets all the expectations of the interface.
When calling handler.register(), MyHandler is passed to the validator (if 
defined in the interface) and if it passes validation will be registered into
the backend.handlers dictionary.  

Using Handlers
--------------

The following are a few examples of working with handlers:

.. code-block:: python

    from cement2.core import handler
    
    # Get a log handler called 'logging'
    handler.get('log', 'logging')
    
    # List all handlers of type 'config'
    handler.list('config')
    
    # Check if an interface called 'output' is defined
    handler.defined('output')
    
    # Check if the handler 'argparse' is registered to the 'argument' interface
    handler.enabled('argument', 'argparse')
    
It is important to note that handlers are stored in backend.handlers as 
uninstantiated objects.  Meaning you must instantiate them after retrieval 
like so:

.. code-block:: python

    from cement2.core import handler
    
    log_handler = handler.get('log', 'logging')
    log = log_handler()
