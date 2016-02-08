Handling Arbitrary Extra Positional Arguments
---------------------------------------------

It is common practice to accept additional positional arguments at command
line, rather than option flags.  For example:

.. code-block:: bash

    $ myapp some-command some-argument --foo=bar


In the above, ``some-command`` would be the function under whatever controller
it is exposed from, and `some-argument` would be just an arbtrary argument.
In most cases, the argument within the code is generic, but its uses vary.
For example:

.. code-block:: bash

    $ myapp create-user john.doe

    $ myapp create-group admins


In the above, the sub-commands are ``create-user`` and ``create-group``, and
in this use case they are under the same controller.  The ``argument`` however
differs for each command, though it is passed to the app the same (the first
positional argument, that is not a controller/command).

The following example outlines how you might handle arbitrary (or generic)
positional arguments.

Example
^^^^^^^

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

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
            base_controller = 'base'
            handlers = [
                MyBaseController,
                MySecondController,
                ]

    def main():
        with MyApp() as app:
            app.run()
        
    if __name__ == '__main__':
        main()


And this would look something like:

.. code-block:: bash

    $ python argtest.py second cmd1 extra1 extra2
    Inside MySecondController.cmd1()
    Extra Argument 0: extra1
    Extra Argument 1: extra2

