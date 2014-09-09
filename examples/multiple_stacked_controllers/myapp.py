
from cement.core import foundation, handler
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

def main():
    try:
        # create the application
        app = foundation.CementApp('myapp')

        # register controllers
        handler.register(MyAppBaseController)
        handler.register(SecondController)
        handler.register(ThirdController)
        handler.register(FourthController)

        # setup the application
        app.setup()

        # run the application
        app.run()
    finally:
        # close the application
        app.close()

if __name__ == '__main__':
    main()
