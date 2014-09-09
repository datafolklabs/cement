
from cement.core import foundation, controller, handler
from cement.core.controller import CementBaseController, expose

class BaseController(CementBaseController):
    class Meta:
        label = 'base'

    @expose()
    def base_cmd1(self):
        print("Inside BaseController.base_cmd1()")

class EmbeddedController(CementBaseController):
    class Meta:
        label = 'embedded'
        description = "embedded with base namespace"
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose()
    def base_cmd2(self):
        print("Inside EmbeddedController.base_cmd2()")

    @expose()
    def embedded_cmd3(self):
        print("Inside EmbeddedController.embedded_cmd3()")

class SecondLevelController(CementBaseController):
    class Meta:
        label = 'second'
        description = ''
        stacked_on = 'base'
        stacked_type = 'nested'

    @expose()
    def second_cmd4(self):
        print("Inside SecondLevelController.second_cmd4()")

    @expose()
    def second_cmd5(self):
        print("Inside SecondLevelController.second_cmd5()")

class ThirdLevelController(CementBaseController):
    class Meta:
        label = 'third'
        description = ''
        stacked_on = 'second'
        stacked_type = 'nested'

    @expose()
    def third_cmd6(self):
        print("Inside ThirdLevelController.third_cmd6()")

    @expose()
    def third_cmd7(self):
        print("Inside ThirdLevelController.third_cmd7()")

class MyApp(foundation.CementApp):
    class Meta:
        label = 'myapp'


def main():
    try:
        # create the app
        app = MyApp()

        # register controllers to the app
        handler.register(BaseController)
        handler.register(EmbeddedController)
        handler.register(SecondLevelController)
        handler.register(ThirdLevelController)

        # setup the app
        app.setup()

        # run the app
        app.run()

    finally:
        # close the app
        app.close()

if __name__ == '__main__':
    main()
