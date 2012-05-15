Examples
========

The following are examples that demonstrate how to handle certain situations
with Cement.

Multiple Stacked and Non-Stacked Controllers
--------------------------------------------

.. code-block:: python


    from cement2.core import foundation, controller, handler

    # define application controllers
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            label = 'base'
            interface = controller.IController
            description = "My Application Does Amazing Things"
            arguments = [
                (['--base-opt'], dict(help="option under base controller")),
                ]

        @controller.expose(help="base controller default command", hide=True)
        def default(self):
            print "Inside MyAppBaseController.default()"
    
        @controller.expose(help="another base controller command")
        def command1(self):
            print "Inside MyAppBaseController.command1()"
        
    class SecondController(controller.CementBaseController):
        """This controller commands are 'stacked' onto the base controller."""
    
        class Meta:
            label = 'second_controller'
            interface = controller.IController
            stacked_on = 'base'
            description = "My Application's Second Controller (stacked)"
            arguments = [
                (['--2nd-opt'], dict(help="another option under base controller")),
                ]
    
        @controller.expose(help="command under the base namespace")
        def command2(self):
            print "Inside SecondController.command2()"
    
    class ThirdController(controller.CementBaseController):
        """This controller commands are *not* 'stacked' onto the base controller."""
    
        class Meta:
            label = 'third_controller'
            interface = controller.IController
            stacked_on = None
            description = "My Application's Third Controller (not-stacked)"
            arguments = [
                (['--3rd-opt'], dict(help="an option only under 3rd controller")),
                ]
    
        @controller.expose(help="default command for third_controller", hide=True)
        def default(self):
            print "Inside ThirdController.default()"
        
        @controller.expose(help="a command only under the 3rd namespace")
        def command3(self):
            print "Inside ThirdController.command3()"
            
    
    class FourthController(controller.CementBaseController):
        """This controller commands are 'stacked' onto the 3rd controller."""
    
        class Meta:
            label = 'fourth_controller'
            interface = controller.IController
            stacked_on = 'third_controller'
            description = "My Application's Fourth Controller (stacked)"
            arguments = [
                (['--4th-opt'], dict(help="an option only under 3rd controller")),
                ]
        
        @controller.expose(help="a command only under the 3rd namespace")
        def command4(self):
            print "Inside FourthController.command4()"
          
    try:
        # create the application
        app = foundation.CementApp('myapp', base_controller=MyAppBaseController)
    
        # register non-base controllers      
        handler.register(SecondController)        
        handler.register(ThirdController)        
        handler.register(FourthController)        

        # setup the application
        app.setup()

        app.run()
    finally:
        app.close()
        
.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    My Application Does Amazing Things

    commands:

      command1
        another base controller command

      command2
        command under the base namespace

      third-controller
        My Application's Third Controller (not-stacked)

    optional arguments:
      -h, --help           show this help message and exit
      --debug              toggle debug output
      --quiet              suppress all output
      --base-opt BASE_OPT  option under base controller
      --2nd-opt 2ND_OPT    another option under base controller
    
    
    $ python myapp.py 
    Inside MyAppBaseController.default()
    
    $ python myapp.py command1
    Inside MyAppBaseController.command1()
    
    $ python myapp.py command2 --2nd-opt=foo
    Inside SecondController.command2()
    
    $ python myapp.py third-controller --3rd-opt=foo
    Inside ThirdController.default()
    
    $ python myapp.py third-controller --help
    usage: myapp.py third_controller <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    My Application's Third Controller (not-stacked)

    commands:

      command3
        a command only under the 3rd namespace

      command4
        a command only under the 3rd namespace

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      --3rd-opt 3RD_OPT  an option only under 3rd controller
      --4th-opt 4TH_OPT  an option only under 3rd controller

    $ python myapp.py third-controller command3 --3rd-opt=foo --4th-opt=bar
    Inside ThirdController.command3()
    
    $ python myapp.py third-controller command4
    Inside FourthController.command4()


Abstract Base Controllers for Shared Arguments and Commands
-----------------------------------------------------------

For larger, complex applications it is often very useful to have abstract
base controllers that hold shared arguments and commands that a number of
other controllers have in common.  Note that in the example below, you can
not override the Meta.arguments in a sub-class or you overwrite the shared
arguments.  That said, you can add any number of additional commands in the
sub-class but still maintain the existing shared commands.

.. code-block:: python

    from cement2.core import foundation, controller, handler
        
    class AbstractBaseController(controller.CementBaseController):
        """
        This is an abstract base class that is useless on its own, but used
        by other classes to sub-class from and to share common commands and
        arguments.
    
        """
        class Meta:
            arguments = [
                ( ['-f', '--foo'], dict(help='notorious foo option')),
                ]
        
        def _setup(self, base_app):
            """
            Add a common object that is useful in multiple sub-classed
            controllers.
        
            """
            super(AbstractBaseController, self)._setup(base_app)
            self.my_shared_obj = dict()
        
        @controller.expose(hide=True)
        def default(self):
            """
            This command will be shared within all controllers that sub-class
            from here.  It can also be overridden in the sub-class, but for
            this example we are making it dynamic.
        
            """
            # do something with self.my_shared_obj here?
            print(self.my_shared_obj)
        
            # or do something with parsed args?
            if self.app.pargs.foo:
                print "Foo option was passed!"
            
            # or maybe do something dynamically
            if self._meta.label == 'controller1':
                # do something for controller1
                print("Inside Controller1.default()")
            else:
                # do something else
                print("Inside %s.default()" % self._meta.label.capitalize())
    
    class MyBaseController(controller.CementBaseController):
        """
        This is the application base controller, but we don't want to use our
        abstract base class here.
    
        """
        class Meta:
            label = 'base'
        
        @controller.expose(hide=True)
        def default(self):
            print("Inside MyBaseController.default()")
        
    class Controller1(AbstractBaseController):
        """
        This controller sub-classes from the abstract base class as to inherite
        shared arguments, and commands.
    
        """
        class Meta:
            label = 'controller1'
            description = 'Controller1 Does Amazing Things'
        
        @controller.expose()
        def command1(self):
            print("Inside Controller1.command1()")
    
    class Controller2(AbstractBaseController):
        """
        This controller also sub-classes from the abstract base class as to 
        inherite shared arguments, and commands.
    
        """
        class Meta:
            label = 'controller2'
            description = 'Controller2 Also Does Amazing Things'
        
        @controller.expose()
        def command2(self):
            print("Inside Controller2.command2()")
    
    app = foundation.CementApp('myapp', base_controller=MyBaseController)

    try:    
        # register non-base controller handlers
        handler.register(Controller1)
        handler.register(Controller2)
    
        app.setup()
        app.run()
    finally:
        app.close()
    
And:

.. code-block:: text

    $ python test.py 
    Inside MyBaseController.default()


    $ python test.py --help
    usage: test.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    Base Controller

    commands:

      controller1
        Controller1 Does Amazing Things

      controller2
        Controller2 Also Does Amazing Things

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
  

    $ python test.py controller1 --help
    usage: test.py controller1 <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    Controller1 Does Amazing Things

    commands:

      command1

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f FOO, --foo FOO  notorious foo option
 

    $ python test.py controller1 command1 
    Inside Controller1.command1()


    $ python test.py controller2 command2
    Inside Controller2.command2()


    $ python test.py controller1 --foo=bar
    {}
    Foo option was passed!
    Inside Controller1.default()


    $ python test.py controller2 --foo=bar
    {}
    Foo option was passed!
    Inside Controller2.default()
