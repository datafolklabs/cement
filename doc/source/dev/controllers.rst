Application Controllers
=======================

Cement defines a controller interface called :ref:`IController <cement2.core.controller>`, 
but does not enable any default handlers that implement the interface.  

Using application controllers is not necessary, but enables rapid development
by wrapping pieces of the framework like adding arguments, and linking 
commands with functions to name a few.  The examples below use the 
CementBaseController for examples.  It is important to note that this class
also requires that your application's argument_handler be the 
ArgParseArgumentHandler.  That said, the CementBaseController is relatively
useless when used directly and therefore should be used as a Base class to
create your own application controllers from.

The following controllers are included and maintained with Cement2:

    * :ref:`CementBaseController <cement2.core.controller>`

Please reference the :ref:`IController <cement2.core.controller>` interface 
documentation for writing your own controller.

    
Example Application Base Controller
-----------------------------------
    
This example demonstrates the use of application controllers that 
handle command dispatch and rapid development.

.. code-block:: python

    from cement2.core import backend, foundation, controller, handler

    # create an application
    app = foundation.lay_cement('example')

    # define an application base controller
    class MyAppBaseController(controller.CementBaseController):
        class meta:
            interface = controller.IController
            label = 'base'
            description = "My Application does amazing things!"

            defaults = dict(
                foo='bar',
                some_other_option='my default value',
                )
            
            arguments = [
                ('--foo', dict(action='store', help='the notorious foo option')),
                ('-C', dict(action='store_true', help='the big C option'))
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
        
        @controller.expose(aliases=['cmd2'], help="more of nothing.")
        def command2(self):
            self.log.info("Inside base.command2 function.")
        
    handler.register(MyAppBaseController)

    # setup the application
    app.setup()

    # run the application
    app.run()

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
      
      
    $ python example2.py 
    INFO: Inside base.default function.
    
    $ python example2.py command1
    INFO: Inside base.command1 function.
    
    $ python example2.py cmd2
    INFO: Inside base.command2 function.