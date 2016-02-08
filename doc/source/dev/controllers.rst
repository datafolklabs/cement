Application Controllers
=======================

Cement defines a controller interface called
:ref:`IController <cement.core.controller>`,
but does not enable any default handlers that implement the interface.

Using application controllers is not necessary, but enables rapid development
by wrapping pieces of the framework like adding arguments, and linking
commands with functions to name a few.  The examples below use the
``CementBaseController`` for examples.  It is important to note that this
class also requires that your application's argument_handler be the
``ArgParseArgumentHandler``.  That said, the ``CementBaseController`` is
relatively useless when used directly and therefore should be used as a Base
class to create your own application controllers from.

The following controllers are included and maintained with Cement:

    * :ref:`CementBaseController <cement.core.controller>`


Please reference the :ref:`IController <cement.core.controller>` interface
documentation for writing your own controller.


Example Application Base Controller
-----------------------------------

This example demonstrates the use of application controllers that
handle command dispatch and rapid development.

.. code-block:: python

    from cement.core import backend,
    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    # define an application base controller
    class MyAppBaseController(CementBaseController):
        class Meta:
            label = 'base'
            description = "My Application does amazing things!"
            epilog = "This is the text at the bottom of --help."

            config_defaults = dict(
                foo='bar',
                some_other_option='my default value',
                )

            arguments = [
                (['-f', '--foo'],
                 dict(action='store', help='the notorious foo option')),
                (['-C'],
                 dict(action='store_true', help='the big c option')),
                ]

        @expose(hide=True, aliases=['run'])
        def default(self):
            self.app.log.info('Inside base.default function.')
            if self.app.pargs.foo:
                self.app.log.info("Recieved option 'foo' with value '%s'." % \
                              self.app.pargs.foo)

        @expose(help="this command does relatively nothing useful.")
        def command1(self):
            self.app.log.info("Inside base.command1 function.")

        @expose(aliases=['cmd2'], help="more of nothing.")
        def command2(self):
            self.app.log.info("Inside base.command2 function.")


    class MyApp(CementApp):
        class Meta:
            label = 'example'
            base_controller = MyAppBaseController


    with MyApp() as app:
        app.run()


As you can see, we're able to build out the core functionality of our app
via a controller class.  Lets see what this looks like:

.. code-block:: text

    $ python example.py --help
    usage: example.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    My Application does amazing things!

    commands:

      command1
        this command does relatively nothing useful.

      command2 (aliases: cmd2)
        more of nothing.

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      --foo FOO   the notorious foo option
      -C          the big C option

    This is the text at the bottom of --help.


    $ python example2.py
    INFO: Inside base.default function.

    $ python example2.py command1
    INFO: Inside base.command1 function.

    $ python example2.py cmd2
    INFO: Inside base.command2 function.


Additional Controllers and Namespaces
-------------------------------------

Any number of additional controllers can be added to your application after a
base controller is created.  Additionally, these controllers can be
``stacked`` onto the base controller (or any other controller) in one of two
ways:

    * ``embedded`` - The controllers commands and arguments are included under
      the parent controllers name space.
    * ``nested`` - The controller label is added as a sub-command under the
      parent controllers namespace (effectively this is a sub-command with
      additional sub-sub-commands under it)


For example, The ``base`` controller is accessed when calling ``example.py``
directly. Any commands under the ``base`` controller would be accessible as
``example.py <cmd1>``, or ``example.py <cmd2>``, etc.  An ``embedded``
controller will merge its commands and options into the ``base`` controller
namespace and appear to be part of the base controller... meaning you would
still access the ``embedded`` controllers commands as
``example.py <embedded_cmd1>``, etc (same for options).

For ``nested`` controllers, a prefix will be created with that controllers
label under its parents namespace.  Therefore you would access that
controllers commands and options as
``example.py <controller_label> <controller_cmd1>``.

See the :ref:`Multiple Stacked Controllers <multiple_stacked_controllers>`
example for more help.
