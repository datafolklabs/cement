Application Cleanup
===================

The concept of 'cleanup' after application run time is nothing new.  What
happens during 'cleanup' all depends on the application.  This might mean
closing and deleting temporary files, removing session data, or deleting a PID
(Process ID) file.

To allow for application cleanup not only within your program, but also
external plugins and extensions, there is the ``app.close()`` function that
must be called after ``app.run()`` regardless of any exceptions or runtime
errors.

For example:

.. code-block:: python

    from cement.core.foundation import CementApp

    app = CementApp('helloworld')
    app.setup()
    app.run()
    app.close()


Calling ``app.close()`` ensures that the ``pre_close`` and ``post_close``
framework hooks are run, allowing extensions/plugins/etc to cleanup after the
program runs.

Note that when using the Python ``with`` operator, the ``setup()`` and
``close()`` methods are automatically called.  For example, the following is
exactly the same as the above example:

.. code-block:: python

    from cement.core.foundation import CementApp

    with CementApp('helloworld') as app:
        app.run()


Also note that you can optionally set an exit code to alter that status in
which your application exits:

.. code-block:: python

    app = CementApp('helloworld')
    app.setup()
    app.run()
    app.close(27)


Or Alternatively:

.. code-block:: python

    with CementApp('helloworld') as app:
        app.run()
        app.exit_code = 123


The default exit code is ``0``, however any uncaught exceptions will cause the
application to exit with a code of ``1`` (error).


Running Cleanup Code
--------------------

Any extension, or plugin, or even the application itself that has 'cleanup'
code should do so within the ``pre_close`` or ``post_close`` hooks to ensure
that it gets run.  For example:

.. code-block:: python

    from cement.core import hook

    def my_cleanup(app):
        # do something when app.close() is called
        pass

    hook.register('pre_close', my_cleanup)
