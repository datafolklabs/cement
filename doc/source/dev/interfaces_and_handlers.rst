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
class have a function called '_setup()'.  Any implementation of that interface
must provide a function called '_setup()', and perform the expected actions
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

    from cement2.core import foundation, interface, handler

    # You must lay_cement() before any handlers can be registered
    app = foundation.lay_cement('myapp')
    
    class MyInterface(interface.Interface):
        class iMeta:
            label = 'myinterface'

        # Must be provided by the implementation
        Meta = interface.Attribute('Handler Meta-data')
        my_var = interface.Attribute('A variable of epic proportions.')
    
        def _setup(config_obj):
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

That said, what is required is an 'iMeta' class that is used to interact
with the interface.  At the very least, this must include a unique 'label'
to identify the interface.  This can also be considered the 'handler type'.  
For example, the ILog interface has a label of 'log'.

Notice that we defined 'Meta' and 'my_var' as Interface Attributes.  This is
a simple identifier that describes an attribute that an implementation is 
expected to provide.

Validating Interfaces
---------------------

A validator call back function can be defined in the interfaces iMeta class
like this:

.. code-block:: python

    from cement2.core import foundation, interface, handler

    # You must lay_cement() before any handlers can be registered
    app = foundation.lay_cement('myapp')
    
    def my_validator(klass, obj):
        members = [
            '_setup',
            'do_something',
            'my_var',
            ]
        interface.validate(MyInterface, obj, members)

    class MyInterface(interface.Interface):
        class iMeta:
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

    from cement2.core import foundation, interface
    
    # You must lay_cement() before any handlers can be registered
    app = foundation.lay_cement('myapp')
    
    class MyHandler(object):
        class Meta:
            interface = MyInterface
            label = 'my_handler'
            description = 'This handler implements MyInterface'
            defaults = {
                foo='bar'
                }
    
        my_var = 'This is my var'
        
        def __init__(self):
            self.config = None
            
        def _setup(config_obj):
            self.config = config_obj
            
        def do_something(self):
            print "Doing work!"

    handler.register(MyHandler)

The above is a simple class that meets all the expectations of the interface.
When calling handler.register(), MyHandler is passed to the validator (if 
defined in the interface) and if it passes validation will be registered into
the cement2.core.backend.handlers dictionary.  

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


Overriding Default Handlers
---------------------------

Cement sets up a number of default handlers for logging, config parsing, etc.
These can be overridden in a number of ways.  The first way is to set the
configuration setting for that handler via the application defaults like so:

.. code-block:: python
    
    from cement2.core import foundation, backend, interface, log
    
    # Set defaults
    defaults = backend.defaults('myapp')
    defaults['base']['log_handler'] = 'mylog'
    
    # Create the application
    app = foundation.lay_cement('myapp', defaults=defaults)
    
    # Define the 'mylog' handler here
    class MyLog(object):
        class Meta:
            interface = log.ILog
            label = 'mylog'
            
        def some_function(self):
            ...
     
    handler.register(MyLog)   
    
    # Setup the application
    app.setup()
    
This may seem a little backwards that we are setting the 'mylog' log_handler
in the default config, and then defining it after the application is created.
The key thing to note is that nothing is actually called until after 
'app.setup()' and also that no handlers can be created until 
'foundation.lay_cement()' is called.  

The second way to override a handler is by passing it to 
'foundation.lay_cement()'.  This is useful if you do not desire to register a
handler (for whatever reason):

.. code-block:: python
    
    from cement2.core import foundation
    from myapp.log import MyLog
    
    app = foundation.lay_cement('myapp', log_handler=MyLog())
    
Some things to note are:

    * The class passed must be instantiated
    * Cement will call ._setup() on the object when app.setup() is called.
    * This handler will *not* be registered in backend.handlers
    

Multiple Registered Handlers
----------------------------

All handlers and interfaces are unique.  In most cases, where the framework
is concerned, only one handler is used.  For example, whatever is configured
for the 'log_handler' will be used and setup as 'app.log'.  However, take for
example an Output handler.  You might have a default output_handler of 
'genshi' (a text templating language) but may also want to override that 
handler with the 'json' output handler when '--json' is passed at command
line.  In order to allow this functionality, both the 'genshi' and 'json'
output handlers must be registered.  

Any number of handlers can be registered to an interface.  You might have a 
use case for an Interface/Handler that may provide different compatibility
base on the operating system, or perhaps based on simply how the application
is called.  A good example would be an application that automates building
packages for Linux distributions.  An interface would define what a build 
handler needs to provide, but the build handler would be different based on
the OS.  The application might have an 'rpm' build handler, or a 'debian' 
build handler to perform the build process differently.
