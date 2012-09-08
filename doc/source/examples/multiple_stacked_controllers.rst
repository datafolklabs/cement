.. _multiple_stacked_controllers:

Multiple Stacked Controllers
----------------------------

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
            self.app.args.parse_args(['--help'])
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
            stacked_type = 'nested'
            description = "My Application's Second Controller (stacked)"
            arguments = [
                (['--2nd-opt'], dict(help="another option under base controller")),
                ]

        @controller.expose(help="command under the base namespace", aliases=['asdfas'])
        def command2(self):
            print "Inside SecondController.command2()"

    class ThirdController(controller.CementBaseController):
        """This controller commands are *not* 'stacked' onto the base controller."""

        class Meta:
            label = 'third_controller'
            interface = controller.IController
            stacked_on = 'second_controller' 
            stacked_type = 'embedded'
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
            stacked_type = 'nested'
            description = "My Application's Fourth Controller (stacked)"
            arguments = [
                (['--4th-opt'], dict(help="an option only under 3rd controller")),
                ]

        @controller.expose(help="a command only under the 3rd namespace")
        def command4(self):
            print "Inside FourthController.command4()"

    try:
        # create the application
        app = foundation.CementApp('myapp')

        # register non-base controllers
        handler.register(MyAppBaseController)
        handler.register(SecondController)
        handler.register(ThirdController)
        handler.register(FourthController)

        # setup the application
        app.setup()

        app.run()
    finally:
        app.close()

In the `base` controller output of `--help` notice that the 
`second-controller` is listed as a sub-command:

.. code-block:: text

    $ python example.py --help
    usage: example.py (sub-commands ...) [options ...] {arguments ...}

    My Application Does Amazing Things

    commands:

      command1
        another base controller command

      second-controller
        My Application's Second Controller (stacked)

    optional arguments:
      -h, --help           show this help message and exit
      --debug              toggle debug output
      --quiet              suppress all output
      --base-opt BASE_OPT  option under base controller
      
      
    $ python example.py command1
    Inside MyAppBaseController.command1()


    $ python example.py second-controller --help
    usage: example.py (sub-commands ...) [options ...] {arguments ...}

    My Application's Second Controller (stacked)

    commands:

      command2 (aliases: asdfas)
        command under the base namespace

      command3
        a command only under the 3rd namespace

      fourth-controller
        My Application's Fourth Controller (stacked)

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      --2nd-opt 2ND_OPT  another option under base controller
      --3rd-opt 3RD_OPT  an option only under 3rd controller

Under the `second-controller` you can see the commands and options from the 
second and third controllers.  In this example, the `second-controller` is
`nested` on the base controller, and the `third-controller` is `embedded` 
on the `second-controller`.  Finally, we see that the `fourth-controller` is
also `nested` on the `second-controller` creating a sub-sub-command.

.. code-block:: text

    $ python example.py second-controller command3
    Inside ThirdController.command3()


    $ python example.py second-controller fourth-controller --help
    usage: example.py (sub-commands ...) [options ...] {arguments ...}

    My Application's Fourth Controller (stacked)

    commands:

      command4
        a command only under the 3rd namespace

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      --4th-opt 4TH_OPT  an option only under 3rd controller


    $ python example.py second-controller fourth-controller command4
    Inside FourthController.command4()
