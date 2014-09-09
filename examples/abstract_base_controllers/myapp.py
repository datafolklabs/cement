
from cement.core import foundation, handler
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

def main():
    # create the app
    app = foundation.CementApp('myapp')

    try:
        # register controllers
        handler.register(MyAppBaseController)
        handler.register(Controller1)
        handler.register(Controller2)

        # setup the app
        app.setup()

        # run it
        app.run()
    finally:
        # close it
        app.close()

if __name__ == '__main__':
    main()
