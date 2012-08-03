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

In Cement, we call the implementation of interfaces 'handlers' and provide the 
ability to easily register, and retrieve them via the :ref:`cement.core.handler`
library.

API References:

    * :ref:`Cement Interface Module <cement.core.interface>`
    * :ref:`Cement Handler Module <cement.core.handler>`
    
    
Defining an Interface
---------------------

Cement uses interfaces and handlers extensively to manage the framework, 
however developers can also make use of this system to provide a clean, and
standardized way of allowing other developers to customize their application.

The following defines a basic interface:

.. code-block:: python

    from cement.core import interface, handler

    class MyInterface(interface.Interface):
        class iMeta:
            label = 'myinterface'

        # Must be provided by the implementation
        Meta = interface.Attribute('Handler Meta-data')
        my_var = interface.Attribute('A variable of epic proportions.')
    
        def _setup(app_obj):
            """
            The setup function is called during application initialization and
            must 'setup' the handler object making it ready for the framework
            or the application to make further calls to it.
        
            Required Arguments:
        
                app_obj
                    The application object.
                
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
For example, the ILog interface has a label of 'log' and any handlers 
registered to that interface are stored in backend.handlers['log'].

Notice that we defined 'Meta' and 'my_var' as Interface Attributes.  This is
a simple identifier that describes an attribute that an implementation is 
expected to provide.

Validating Interfaces
---------------------

A validator call back function can be defined in the interfaces iMeta class
like this:

.. code-block:: python

    from cement.core import interface, handler

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
the validator is called and the handler object is passed to the validator.  In
the above example, we simply define what members we want to validate for and
then call interface.validate() which will raise 
cement.core.exc.InterfaceError if validation fails.  It is not 
necessary to use interface.validate() but it is useful and recommended.  In 
general, the key thing to note is that a validator either raises 
InterfaceError or does nothing if validation passes.

Registering Handlers to an Interface
------------------------------------

An interface simply defines what an implementation is expected to provide, 
where a handler actually implements the interface.  The following example
is a handler that implements the MyInterface above:

.. code-block:: python

    from cement.core import handler
    from myapp.interfaces import MyInterface
    
    class MyHandler(object):
        class Meta:
            interface = MyInterface
            label = 'my_handler'
            description = 'This handler implements MyInterface'
            config_defaults = {
                foo='bar'
                }
    
        my_var = 'This is my var'
        
        def __init__(self):
            self.app = None
            
        def _setup(app_obj):
            self.app = app_obj
            
        def do_something(self):
            print "Doing work!"

    handler.register(MyHandler)

The above is a simple class that meets all the expectations of the interface.
When calling handler.register(), MyHandler is passed to the validator (if 
defined in the interface) and if it passes validation will be registered into
the cement.core.backend.handlers dictionary.  

Using Handlers
--------------

The following are a few examples of working with handlers:

.. code-block:: python

    from cement.core import handler
    
    # Get a log handler called 'logging'
    log_handler = handler.get('log', 'logging')
    log = log_handler()
    
    # List all handlers of type 'config'
    handler.list('config')
    
    # Check if an interface called 'output' is defined
    handler.defined('output')
    
    # Check if the handler 'argparse' is registered to the 'argument' interface
    handler.registered('argument', 'argparse')
    
It is important to note that handlers are stored in backend.handlers as 
uninstantiated objects.  Meaning you must instantiate them after retrieval 
like so:

.. code-block:: python

    from cement.core import handler
    
    log_handler = handler.get('log', 'logging')
    log = log_handler()

Or shorter:

.. code-block:: python

    log = handler.get('log', 'logging')()


Overriding Default Handlers
---------------------------

Cement sets up a number of default handlers for logging, config parsing, etc.
These can be overridden in a number of ways.  The first way is by passing 
them as keyword arguments to CementApp():

.. code-block:: python
    
    from cement.core import foundation
    from myapp.log import MyLogHandler
    
    # Create the application
    app = foundation.CementApp('myapp', log_handler=MyLogHandler)
    
The second way to override a handler is by setting it directly in the 
CementApp meta data:

.. code-block:: python
    
    from cement.core import foundation
    from myapp.log import MyLogHandler
    
    class MyApp(foundation.CementApp):
        class Meta:
            label = 'myapp'
            log_handler = MyLogHandler

    app = MyApp()
    
There are times that you may want to pre-instantiate handlers before 
passing them to CementApp().  The following works just the same:

.. code-block:: python
    
    from cement.core import foundation
    from myapp.log import MyLogHandler
    
    my_log = MyLogHandler(some_param='some_value')
    
    class MyApp(foundation.CementApp):
        class Meta:
            label = 'myapp'
            log_handler = my_log

    app = MyApp()

To see what default handlers can be overridden, see the 
:ref:`cement.core.foundation <cement.core.foundation>` documentation.

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

Customizing Handlers
--------------------

The most common way to customize a handler is to subclass it, and then pass
it to CementApp():

.. code-block:: python

    from cement.core import foundation
    from cement.lib.ext_logging import LoggingLogHandler
    
    class MyLogHandler(LoggingLogHandler):
        class Meta:
            label = 'mylog'
            
        def info(self, msg):
            # do something to customize this function, here...
            super(MyLogHandler, self).info(msg)
            
    app = foundation.CementApp('myapp', log_handler=MyLogHandler)
    
Hander Default Configuration Settings
-------------------------------------

All handlers can define default config file settings via the 'config_defaults' 
meta option.  These will be merged into the app.config under the 
'<handler_interface>.<handler_label>' section.  These settings are overridden 
in the following order.  

 * The config_defaults dictionary passed to CementApp()
 * Via any application config files with a 
   [<handler_interface>.<handler_type>] block
 
The following shows how to override defaults by passing them with the defaults
dictionary to CementApp():
            
The first way is to pass the overrides via the config_defaults dictionary 
passed to the CementApp().

.. code-block:: python

    from cement.core import foundation, backend

    defaults = backend.defaults('myinterface.myhandler')
    defaults['myinterface.myhandler'] = dict(foo='bar')
    app = foundation.CementApp('myapp', config_defaults=defaults)

Cement will use all defaults set via MyHandler.Meta.config_defaults (for this
example), and then override just what is passed via 
config_defaults['myinterface.myhandler'].  You should use this approach only 
to modify the global defaults for your application.  The second way is to then 
set configuration file defaults under the [myinterface.myhandler] section.  
For example:

*my.config*

.. code-block:: text

    [myinterface.myhandler]
    foo = bar

In the real world this may look like '[controller.tasks]', or 
'[database.mysql]' depending on what the interface label, and handler label's
are.  Additionally, individual handlers can override their config section
by setting Meta.config_section.
