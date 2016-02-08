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

    from cement.core.foundation import CementApp
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

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            handlers = [
                MyAppBaseController,
                UsersController,
                HostsController,
                UsersListController,
                HostsListController,
                ]

    def main():
        with MyApp() as app:
            app.run()

    if __name__ == '__main__':
        main()

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    Base Controller

    commands:

      hosts
        this is the hosts controller

      users
        this is the users controller

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


    $ python myapp.py users --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    this is the users controller

    commands:

      list
        list all available users

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


    $ python myapp.py users list
    Inside UsersListController.default()

    $ python myapp.py hosts list
    Inside HostsListController.default()

