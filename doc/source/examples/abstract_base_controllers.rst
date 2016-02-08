Abstract Base Controllers for Shared Arguments and Commands
-----------------------------------------------------------

For larger, complex applications it is often very useful to have abstract
base controllers that hold shared arguments and commands that a number of
other controllers have in common.  Note that in the example below, you can
not override the Meta.arguments in a sub-class or you overwrite the shared
arguments, but it is possible to `append` to them in order to maintain the
defaults while having unique options/arguments for the sub-classed controller.
As well, you can add any number of additional commands in the sub-class but
still maintain the existing shared commands (or override them as necessary).

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose


    class AbstractBaseController(CementBaseController):
        """
        This is an abstract base class that is useless on its own, but used
        by other classes to sub-class from and to share common commands and
        arguments.  This should not be confused with the `MyAppBaseController`
        used as the ``base_controller`` namespace.

        """
        class Meta:
            stacked_on = 'base'
            stacked_type = 'nested'
            arguments = [
                ( ['-f', '--foo'], dict(help='notorious foo option')),
                ]

        def _setup(self, base_app):
            super(AbstractBaseController, self)._setup(base_app)

            # add a common object that will be used in any sub-class
            self.reusable_dict = dict()

        @expose(hide=True)
        def default(self):
            """
            This command will be shared within all controllers that sub-class
            from here.  It can also be overridden in the sub-class, but for
            this example we are making it dynamic.

            """
            # do something with self.my_shared_obj here?
            if 'some_key' in self.reusable_dict.keys():
                pass

            # or do something with parsed args?
            if self.app.pargs.foo:
                print "Foo option was passed with value: %s" % self.app.pargs.foo

            # or maybe do something dynamically
            print("Inside %s.default()" % self.__class__.__name__)

    class MyAppBaseController(CementBaseController):
        """
        This is the application base controller, but we don't want to use our
        abstract base class here.

        """
        class Meta:
            label = 'base'

        @expose(hide=True)
        def default(self):
            print("Inside MyAppBaseController.default()")

    class Controller1(AbstractBaseController):
        """
        This controller sub-classes from the abstract base class as to inherite
        shared arguments, and commands.

        """
        class Meta:
            label = 'controller1'

        @expose()
        def command1(self):
            print("Inside Controller1.command1()")

    class Controller2(AbstractBaseController):
        """
        This controller also sub-classes from the abstract base class as to
        inherite shared arguments, and commands.

        """
        class Meta:
            label = 'controller2'

        @expose()
        def command2(self):
            print("Inside Controller2.command2()")


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            base_controller = 'base'
            handlers = [
                MyAppBaseController,
                Controller1,
                Controller2,
                ]

    def main():
        with MyApp() as app:
            app.run()

    if __name__ == '__main__':
        main()

And:

.. code-block:: text

    $ python myapp.py
    Inside MyAppBaseController.default()

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    Base Controller

    commands:

      controller1
        Controller1 Controller

      controller2
        Controller2 Controller

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


    $ python myapp.py controller1
    Inside Controller1.default()

    $ python myapp.py controller1 --foo=bar
    Foo option was passed with value: bar
    Inside Controller1.default()

    $ python myapp.py controller2
    Inside Controller2.default()

