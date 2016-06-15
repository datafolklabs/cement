Application Design
==================

Cement does not enforce any form of application layout, or design.  That said,
there are a number of best practices that can help newcomers get settled into
using Cement as a foundation to build their application.

Single File Scripts
-------------------

Cement can easily be used for quick applications and scripts that are based
out of a single file.  The following is a minimal example that creates a
``CementApp`` with several sub-commands:

.. code-block:: python


    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose


    class BaseController(CementBaseController):
        class Meta:
            label = 'base'
            description = "MyApp Does Amazing Things"
            arguments = [
                (['-f, '--foo'], dict(help='notorious foo option')),
                (['-b', '--bar'], dict(help='infamous bar option')),
                ]

        @expose(hide=True)
        def default(self):
            print("Inside MyAppBaseController.default()")

        @expose(help="this is some help text about the cmd1")
        def cmd1(self):
            print("Inside BaseController.cmd1()")

        @expose(help="this is some help text about the cmd2")
        def cmd2(self):
            print("Inside BaseController.cmd2()")

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            base_controller = BaseController


    def main():
        with MyApp() as app:
            app.run()

    if __name__ == '__main__':
        main()


In this example, we've defined a base controller to handler the heavy lifting
of what this script does, while providing sub-commands to handler different
tasks.  We've also included a number of command line arguments/options that
can be used to alter how the script operates, and to allow user input.

Notice that we have defined a ``main()`` function, and then beyond that
where we call ``main()`` if ``__name__`` is ``__main__``.  This essentially
says, if the script was called directly (not imported by another Python
library) then execute the ``main()`` function.


Multi-File Applications
-----------------------

Larger applications need to be properly organized to keep code clean, and to
keep a high level of maintainability (read: to keep things from getting
shitty). `The Boss Project <https://boss.readthedocs.io>`_ provides our recommended
application layout, and is a great starting point for anyone new to Cement.

The primary detail about how to layout your code is this:  All CLI/Cement
related code should live separate from the "core logic" of your application.
Most likely, you will have some code that is re-usable by other people and you
do not want to mix this with your Cement code, because that will rely on
Cement being loaded to function properly (like it is when called from command
line).

For this reason, we recommend a structure similar to the following:

.. code-block:: text

    - myapp/
    - myapp/cli
    - myapp/core


All code related to your CLI, which relies on Cement, should live in
``myapp/cli/``, and all code that is the "core logic" of your application
should live in a module like ``myapp/core``.  The idea being that, should
anyone wish to re-use your library, they should not be required to run your
CLI application to do so.  You want people to be able to do the following:

.. code-block:: python

    from yourapp.core.some_library import SomeClass


The ``SomeClass`` should not rely on ``CementApp`` (i.e. the ``app`` object).
In this case, the code under ``myapp/cli/`` would import from ``myapp/core/``
and add the "CLI" stuff on top of it.

In short, the CLI code should handle interaction with the user via the shell,
and the core code should handle application logic un-reliant on the CLI being
loaded.

See the :ref:`Starting Projects from Boss Templates <boss>` section for more
info on using Boss.


Handling High Level Exceptions
------------------------------

The following expands on the above to give an example of how you might handle
exceptions at the highest level (wrapped around the app object).  It is very
well known that exception handling should happen as close to the source of the
exception as possible, and you should do that.  However at the top level
(generally in your ``main.py`` or similar) you want to handle certain
exceptions (such as argument errors, or user interaction related errors) so
that they are presented nicely to the user.  End-users don't like stack
traces!

The below example catches common framework exceptions that Cement might throw,
but you could also catch your own application specific exception this way:

.. code-block:: python

    import sys

    from cement.core.foundation import CementApp
    from cement.core.exc import FrameworkError, CaughtSignal


    def main():
        with CementApp('myapp') as app:
            try:
                app.run()

            except CaughtSignal as e:
                # determine what the signal is, and do something with it?
                from signal import SIGINT, SIGABRT

                if e.signum == SIGINT:
                    # do something... maybe change the exit code?
                    app.exit_code = 110
                elif e.signum == SIGABRT:
                    # do something else...
                    app.exit_code = 111

            except FrameworkError as e:
                # do something when a framework error happens
                print("FrameworkError => %s" % e)

                # and maybe set the exit code to something unique as well
                app.exit_code = 300

            finally:
                # Maybe we want to see a full-stack trace for the above
                # exceptions, but only if --debug was passed?
                if app.debug:
                    import traceback
                    traceback.print_exc()

    if __name__ == '__main__':
        main()
