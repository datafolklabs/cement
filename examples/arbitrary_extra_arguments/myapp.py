
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler

class MyBaseController(CementBaseController):
    class Meta:
        label = 'base'

class MySecondController(CementBaseController):
    class Meta:
        label = 'second'
        stacked_type = 'nested'
        stacked_on = 'base'
        description = 'this is the second controller namespace'
        arguments = [
            (['-f', '--foo'],
             dict(help='the notorious foo option', action='store')),
            (['extra_arguments'],
             dict(action='store', nargs='*')),
        ]

    @expose()
    def cmd1(self):
        print "Inside MySecondController.cmd1()"

        if self.app.pargs.extra_arguments:
            print "Extra Argument 0: %s" % self.app.pargs.extra_arguments[0]
            print "Extra Argument 1: %s" % self.app.pargs.extra_arguments[1]


class MyApp(CementApp):
    class Meta:
        label = 'myapp'
        base_controller = MyBaseController

def main():
    app = MyApp()
    handler.register(MySecondController)

    try:
        app.setup()
        app.run()
    finally:
        app.close()

if __name__ == '__main__':
    main()
