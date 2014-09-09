
from cement.core import foundation, handler
from cement.core.controller import CementBaseController, expose

# define application controllers
class MyAppBaseController(CementBaseController):
    class Meta:
        label = 'base'

class UsersController(CementBaseController):
    class Meta:
        label = 'users'
        description = "this is the users controller"
        stacked_on = 'base'
        stacked_type = 'nested'

class HostsController(CementBaseController):
    class Meta:
        label = 'hosts'
        description = "this is the hosts controller"
        stacked_on = 'base'
        stacked_type = 'nested'

class UsersListController(CementBaseController):
    class Meta:
        label = 'users_list'
        description = 'list all available users'
        aliases = ['list']
        aliases_only = True
        stacked_on = 'users'
        stacked_type = 'nested'

    @expose(hide=True)
    def default(self):
        print "Inside UsersListController.default()"

class HostsListController(CementBaseController):
    class Meta:
        label = 'hosts_list'
        description = 'list all available hosts'
        aliases = ['list']
        aliases_only = True
        stacked_on = 'hosts'
        stacked_type = 'nested'

    @expose(hide=True)
    def default(self):
        print "Inside HostsListController.default()"

def main():
    try:
        # create the application
        app = foundation.CementApp('myapp')

        # register non-base controllers
        handler.register(MyAppBaseController)
        handler.register(UsersController)
        handler.register(HostsController)
        handler.register(UsersListController)
        handler.register(HostsListController)

        # setup the application
        app.setup()

        # run it
        app.run()
    finally:
        # close it
        app.close()

if __name__ == '__main__':
    main()
