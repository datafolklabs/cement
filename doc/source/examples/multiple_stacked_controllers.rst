.. _multiple_stacked_controllers:

Multiple Stacked Controllers
----------------------------

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    # define application controllers
    class MyAppBaseController(CementBaseController):
        class Meta:
            label = 'base'
            description = "my application does amazing things"
            arguments = [
                (['--base-opt'], dict(help="option under base controller")),
                ]

        @expose(help="base controller default command", hide=True)
        def default(self):
            print "Inside MyAppBaseController.default()"

        @expose(help="another base controller command")
        def command1(self):
            print "Inside MyAppBaseController.command1()"

    class SecondController(CementBaseController):
        class Meta:
            label = 'second_controller'
            stacked_on = 'base'
            stacked_type = 'nested'
            description = "this is the second controller (stacked/nested on base)"
            arguments = [
                (['--2nd-opt'], dict(help="another option under base controller")),
                ]

        @expose(help="second-controller default command", hide=True)
        def default(self):
            print "Inside SecondController.default()"

        @expose(help="this is a command under the second-controller namespace")
        def command2(self):
            print "Inside SecondController.command2()"

    class ThirdController(CementBaseController):
        class Meta:
            label = 'third_controller'
            stacked_on = 'second_controller'
            stacked_type = 'embedded'
            description = "this controller is embedded in the second-controller"
            arguments = [
                (['--3rd-opt'], dict(help="an option only under 3rd controller")),
                ]

        @expose(help="another command under the second-controller namespace")
        def command3(self):
            print "Inside ThirdController.command3()"

    class FourthController(CementBaseController):
        class Meta:
            label = 'fourth_controller'
            stacked_on = 'second_controller'
            stacked_type = 'nested'
            description = "this controller is nested on the second-controller"
            arguments = [
                (['--4th-opt'], dict(help="an option only under 3rd controller")),
                ]

        @expose(help="a command only under the fourth-controller namespace")
        def command4(self):
            print "Inside FourthController.command4()"

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            handlers = [
                MyAppBaseController,
                SecondController,
                ThirdController,
                FourthController,
                ]

    def main():
        with MyApp() as app:
            app.run()
            

    if __name__ == '__main__':
        main()


In the `base` controller output of `--help` notice that the
`second-controller` is listed as a sub-command:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    my application does amazing things

    commands:

      command1
        another base controller command

      second-controller
        this is the second controller (stacked/nested on base)

    optional arguments:
      -h, --help           show this help message and exit
      --debug              toggle debug output
      --quiet              suppress all output
      --base-opt BASE_OPT  option under base controller


    $ python myapp.py
    Inside MyAppBaseController.default()


    $ python myapp.py command1
    Inside MyAppBaseController.command1()

    $ python myapp.py second-controller
    Inside SecondController.default()

    $ python myapp.py second-controller --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    this is the second controller (stacked/nested on base)

    commands:

      command2
        this is a command under the second-controller namespace

      command3
        another command under the second-controller namespace

      fourth-controller
        this controller is nested on the second-controller

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

    $ python myapp.py second-controller command3
    Inside ThirdController.command3()


    $ python myapp.py second-controller fourth-controller --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    this controller is nested on the second-controller

    commands:

      command4
        a command only under the fourth-controller namespace

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      --4th-opt 4TH_OPT  an option only under 3rd controller


    $ python myapp.py second-controller fourth-controller command4
    Inside FourthController.command4()
