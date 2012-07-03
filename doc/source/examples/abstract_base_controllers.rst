Abstract Base Controllers for Shared Arguments and Commands
-----------------------------------------------------------

For larger, complex applications it is often very useful to have abstract
base controllers that hold shared arguments and commands that a number of
other controllers have in common.  Note that in the example below, you can
not override the Meta.arguments in a sub-class or you overwrite the shared
arguments.  That said, you can add any number of additional commands in the
sub-class but still maintain the existing shared commands.

.. code-block:: python

    from cement.core import foundation, controller, handler
        
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
