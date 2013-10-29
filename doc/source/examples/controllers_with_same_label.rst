.. _controllers_with_same_label:

Multiple Controllers With Same Label
------------------------------------

There are many ways to use controllers.  In some circumstances you might find
that you want to have two controllers with the same label but stacked on
different parent controllers.  This is a problem because controller labels
must be unique.

Take for example the situation where you want to have a 'list' controller,
rather than a 'list' function of another controller.  You might call this
as:

.. code-block:: text

    $ myapp <controller1> <list_controller>

    $ myapp <controller2> <some_other_list_controller>


In both cases, you would probably want the 'sub-controller' or sub-command to
be 'list'.  This is possible with the use of the 'aliases' and 'aliases_only'
Meta options.  Take the following code as an example where we have a 'users'
and a 'hosts' controller and we want to have a 'list' sub-command under both:

.. code-block:: python

    from cement.core import foundation, controller, handler

    # define application controllers
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            label = 'base'

    class UsersController(controller.CementBaseController):
        class Meta:
            label = 'users'
            stacked_on = 'base'
            stacked_type = 'nested'

    class HostsController(controller.CementBaseController):
        class Meta:
            label = 'hosts'
            stacked_on = 'base'
            stacked_type = 'nested'

    class UsersListController(controller.CementBaseController):
        class Meta:
            label = 'users_list'
            description = 'list all available users'
            aliases = ['list']
            aliases_only = True
            stacked_on = 'users'
            stacked_type = 'nested'

        @controller.expose(hide=True)
        def default(self):
            print "Inside UsersListController.default()"

    class HostsListController(controller.CementBaseController):
        class Meta:
            label = 'hosts_list'
            description = 'list all available hosts'
            aliases = ['list']
            aliases_only = True
            interface = controller.IController
            stacked_on = 'hosts'
            stacked_type = 'nested'

        @controller.expose(hide=True)
        def default(self):
            print "Inside HostsListController.default()"

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

        app.run()
    finally:
        app.close()

.. code-block:: text

    $ myapp --help
    usage: myapp (sub-commands ...) [options ...] {arguments ...}

    Base Controller

    commands:

      hosts
        Hosts Controller

      users
        Users Controller

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


    $ myapp users --help
    usage: myapp (sub-commands ...) [options ...] {arguments ...}

    Users Controller

    commands:

      list
        list all available users

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


    $ myapp hosts --help
    usage: myapp (sub-commands ...) [options ...] {arguments ...}

    Hosts Controller

    commands:

      list
        list all available hosts

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


    $ myapp users list
    Inside UsersListController.default()


    $ myapp hosts list
    Inside HostsListController.default()
