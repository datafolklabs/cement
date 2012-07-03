Application Controllers
=======================

Cement defines a controller interface called :ref:`IController <cement.core.controller>`, 
but does not enable any default handlers that implement the interface.  

Using application controllers is not necessary, but enables rapid development
by wrapping pieces of the framework like adding arguments, and linking 
commands with functions to name a few.  The examples below use the 
CementBaseController for examples.  It is important to note that this class
also requires that your application's argument_handler be the 
ArgParseArgumentHandler.  That said, the CementBaseController is relatively
useless when used directly and therefore should be used as a Base class to
create your own application controllers from.

The following controllers are included and maintained with Cement:

    * :ref:`CementBaseController <cement.core.controller>`

Please reference the :ref:`IController <cement.core.controller>` interface 
documentation for writing your own controller.

    
Example Application Base Controller
-----------------------------------
    
This example demonstrates the use of application controllers that 
handle command dispatch and rapid development.

.. code-block:: python

    from cement.core import backend, foundation, controller, handler

    # define an application base controller
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            label = 'base'
            description = "My Application does amazing things!"
            epilog = "This is the text at the bottom of --help."
            
            config_defaults = dict(
                foo='bar',
                some_other_option='my default value',
                )
            
            arguments = [
                (['-f', '--foo'], dict(action='store', help='the notorious foo option')),
                (['-C'], dict(action='store_true', help='the big C option'))
                ]
        
        @controller.expose(hide=True, aliases=['run'])
        def default(self):
            self.log.info('Inside base.default function.')
            if self.pargs.foo:
                self.log.info("Recieved option 'foo' with value '%s'." % \
                              self.pargs.foo)
                          
        @controller.expose(help="this command does relatively nothing useful.")
        def command1(self):
            self.log.info("Inside base.command1 function.")
        
        @controller.expose(aliases=['cmd2'], help="more of nothing.")
        def command2(self):
            self.log.info("Inside base.command2 function.")
    
    # create an application
    app = foundation.CementApp('example', base_controller=MyAppBaseController)

    try:
        # setup the application
        app.setup()
        
        # run the application
        app.run()
    finally:
        # close the application
        app.close()
    
As you can see, we're able to build out the core functionality of our app
via a controller class.  Lets see what this looks like:

.. code-block:: text

    $ python example2.py --help
    usage: example2.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    My Application does amazing things!

    commands:

      command1
        this command does relatively nothing useful.

      command2 (aliases: cmd2)
        more of nothing.

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      --foo FOO   the notorious foo option
      -C          the big C option
      
    This is the text at the bottom of --help.
    
    
    $ python example2.py 
    INFO: Inside base.default function.
    
    $ python example2.py command1
    INFO: Inside base.command1 function.
    
    $ python example2.py cmd2
    INFO: Inside base.command2 function.


Additional Controllers and Namespaces
-------------------------------------

Any number of additional controllers can be added to your application after a
base controller is created.  Additionally, these controllers can either be
'stacked' onto the base controller namespace, or can have their own namespace.

For example, the 'base' controller is accessed when calling 'example.py' 
directly. Any commands under the 'base' controller would be accessible as
'example.py <cmd1>', or 'example.py <cmd2>', etc.  A 'stacked' controller will
merge its commands and options into the 'base' controller namespace and appear
to be part of the base controller... meaning you would still access the 
stacked controllers commands as 'example.py <stacked_cmd1>', etc (same for
options).  

For controllers that are not 'stacked', a prefix will be created with that
controllers label.  Therefore you would access that controllers commands and
options as 'example.py <controller_label> <controller_cmd1>'.

The following example implements two additional controllers.  One is 'stacked'
and the other is not.  Pay attention to how this looks at the command line:

.. code-block:: python

    from cement.core import backend, foundation, controller, handler

    # define an application base controller
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            label = 'base'
            description = "My Application does amazing things!"

            config_defaults = dict(
                foo='bar',
                some_other_option='my default value',
                )

            arguments = [
                (['-f', '--foo'], dict(action='store', help='the notorious foo option')),
                (['-C'], dict(action='store_true', help='the big C option')),
                ]

        @controller.expose(hide=True, aliases=['run'])
        def default(self):
            self.log.info('Inside base.default function.')
            if self.pargs.foo:
                self.log.info("Recieved option 'foot' with value '%s'." % \
                              self.pargs.foo)

        @controller.expose(help="this command does relatively nothing useful.")
        def command1(self):
            self.log.info("Inside base.command1 function.")

    class Controller2(controller.CementBaseController):
        class Meta:
            label = 'controller2'
            stacked_on = 'base'
            description = 'This is the description for controller2.'
            config_defaults = dict()

            arguments = [
                (['--foo2'], dict(action='store', help='the notorious foo option')),
                ]

        @controller.expose(hide=False, help='A command from a stacked controller')
        def command2(self):
            self.log.info('Inside controller2.command2 function.')

    class Controller3(controller.CementBaseController):
        class Meta:
            label = 'controller3'
            description = 'This is the description for controller3.'
            config_defaults = dict()

            arguments = [
                (['--foo3'], dict(action='store', help='the notorious foo option')),
                ]

        @controller.expose(hide=True)
        def default(self):
            print 'Inside controller3.default function.'
        
        @controller.expose(hide=False, help='A command under controller3')
        def command3(self):
            self.log.info('Inside controller3.command3 function.')

    # create an application
    app = foundation.CementApp('example', base_controller=MyAppBaseController)
    
    # register non-base controllers
    handler.register(Controller2)
    handler.register(Controller3)

    try:
        # setup the application
        app.setup()
        
        # run the application
        app.run()
    finally:
        # close the application
        app.close()

From our 'base' namespace this looks like:

.. code-block:: text

    $ python test.py --help
    usage: test.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    My Application does amazing things!

    commands:

      command1
        this command does relatively nothing useful.

      command2
        A command from a stacked controller

      controller3
        This is the description for controller3.

    optional arguments:
      -h, --help   show this help message and exit
      --debug      toggle debug output
      --quiet      suppress all output
      --foo FOO    the notorious foo option
      -C           the big C option
      --foo2 FOO2  the notorious foo option
      
Notice that 'command1' and the '--foo' option are from the base controller.
However, 'command2' and '--foo2' are from Controller2 but because that 
controller is 'stacked_on' the 'base' controller... those commands and options
appear to be part of base.  Finally, take note that 'controller3' is added
as another command however this is a special command in that it provides 
access to the 'controller3' namespace.

.. code-block:: text

    $ python test.py controller3 --help
    usage: test.py controller3 <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    This is the description for controller3.

    commands:

      command3
        A command under controller3

    optional arguments:
      -h, --help   show this help message and exit
      --debug      toggle debug output
      --quiet      suppress all output
      --foo3 FOO3  the notorious foo option

As we can see, under the 'controller3' namespace we only have our 'command3'
and '--foo3' option created under Controller3.

Whether to use 'stacked' controllers, or subcontroller namespaces is 
completely up to you and really depends on the application.

Note: Controllers can be stacked upon other controllers that are also stacked.
For example if Controller1 is stacked on the base controller, and 
Controller2 is stacked on Controller1... then the commands and arguments for
Controller2 will also appear under the 'base' namespace.
