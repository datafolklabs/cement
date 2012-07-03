Multiple Stacked and Non-Stacked Controllers
--------------------------------------------

.. code-block:: python


    from cement.core import foundation, controller, handler

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


