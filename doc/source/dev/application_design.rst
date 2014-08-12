Application Design
==================

Cement does not enforce any form of application layout, or design.  That said,
there are a number of best practices that can help newcomers get settled into
using Cement as a foundation to build their application.

Single File Scripts
-------------------

Cement can easily be used for quick applications and scripts that are based
out of a single file.  The following is a minimal example that creates a
CementApp with several sub-commands:

.. code-block:: python


    from cement.core import foundation
    from cement.core.controller import CementBaseController, expose


    class BaseController(CementBaseController):
        class Meta:
            label = 'base'
            description = "MyApp Does Amazing Things"

        @expose(hide=True)
        def default(self):
            print("Inside MyAppBaseController.default()")

        @expose(help="this is some help text about the cmd1")
        def cmd1(self):
            print("Inside BaseController.cmd1()")

        @expose(help="this is some help text about the cmd2")
        def cmd2(self):
            print("Inside BaseController.cmd2()")

    class MyApp(foundation.CementApp):
        class Meta:
            label = 'myapp'
            base_controller = BaseController


    def main():
        # create the app - before the try/except/finally block
        app = MyApp()

        try:
            # setup the app
            app.setup()

            # run the app
            app.run()

        finally:
            # close the app
            app.close()

    if __name__ == '__main__':
        main()


In this example, we've defined a base controller to handler the heavy lifting
of what this script does, while providing sub-commands to handler different
tasks.  This is then attached to the `MyApp` application object.

Notice that we have defined a `main()` function, and then the beyond that
where we call `main()` if `__name__` is `__main__`.  This essentially says, if
the script was called directly (not imported by another Python library) then
execute the `main()` function.


Multi-File Applications
-----------------------

Larger applications need to be properly organized to keep code clean, and to
keep a high level of maintainability (read: to keep things from getting
shitty). `The Boss Project <http://boss.rtfd.org>`_ provides our recommended
application layout, and is a great starting point for anyone new to Cement.

The primary detail about how to layout your code is this:  All CLI/Cement
related code should live separate from the "core logic".  Most likely, you
will have some code that is re-usable by other people.  You do not want to mix
this with your Cement code, becuase that will rely on Cement being loaded to
function properly.

For this reason, we recommend a structure similar to the following:

.. code-block:: text

    - myapp/
    - myapp/cli
    - myapp/core


All code related to your CLI, which relies on Cement, should live in
`myapp/cli/`, and all code that is the "core logic" of your application
should live in a module like `myapp/core`.  The idea being that, should anyone
wish to re-use your library, they should not be required to run your CLI
application to do so.  You want people to be able to do the following:

.. code-block:: python

    from yourapp.core.some_library import SomeClass

The `SomeClass` should not rely on your CementApp object (i.e. `app` object).
In this case, the code under `myapp/cli/` would import from `myapp/core/` and
add the "CLI" stuff on top of it.

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
(generally in your main.py or similar) you want to handle the exception so
that they are presented nicely to the user.  End-users don't like stack
traces!

The below example catches common framework exceptions that Cement might throw:

.. code-block:: python

    import sys
    from cement.core.exc import FrameworkError, CaughtSignal
    from cement.core.foundation import CementApp

    def main():
        # create the app
        app = CementApp('myapp')

        # default our exit status (return code) to 0 (non-error)
        ret = 0

        try:
            # setup the app
            app.setup()

            # run the app
            app.run()

        except CaughtSignal as e:
            # note: this is more commonly handled with the `signal` hook,
            # however some use cases might want to handle signals at the top
            # level for example, to change the exit status (like below), etc.

            # maybe determine what the signal is, and do something with it?
            from signal import SIGINT, SIGABRT

            if e.signum == SIGINT:
                # do something... maybe change the return status
                ret = 110
            elif e.signum == SIGABRT:
                # do something else...
                ret = 111

        except FrameworkError as e:
            # do something when a framework error happens
            print("FrameworkError => %s" % e)

            # set the exit status to 1 (error)
            ret = 1

        finally:
            # if --debug was passed, we want to see a full stack trace
            if app.debug:
                import traceback
                print("")
                print('TRACEBACK:')
                print('-' * 77)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=20, file=sys.stdout)
                print("")

            # allow everything to cleanup nicely, and exit with out custom
            # error code
            app.close(ret)

    if __name__ == '__main__':
        main()
