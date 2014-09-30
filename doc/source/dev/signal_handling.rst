Signal Handling
===============

Python provides the `Signal <http://docs.python.org/library/signal.html>`_
library allowing developers to catch Unix signals and set handlers for
asynchronous events.  For example, the 'SIGTERM' (Terminate) signal is
received when issuing a 'kill' command for a given Unix process.  Via the
signal library, we can set a handler (function) callback that will be executed
when that signal is received.  Some signals however can not be handled/caught,
such as the SIGKILL signal (kill -9).  Please refer to the
`Signal <http://docs.python.org/library/signal.html>`_ library documentation
for a full understanding of its use and capabilities.

A caveat when setting a signal handler is that only one handler can be defined
for a given signal.  Therefore, all handling must be done from a single
callback function.  This is a slight roadblock for applications built on
Cement in that many pieces of the framework are broken out into independent
extensions as well as applications that have 3rd party plugins.  The trouble
happens when the application, plugins, and framework extensions all need to
perform some action when a signal is caught.  This section outlines the
recommended way of handling signals with Cement versus manually setting signal
handlers that may.

*Important Note*

It is important to note that it is not necessary to use the Cement mechanisms
for signal handling, what-so-ever.  That said, the primary concern of the
framework is that app.close() is called no matter what the situation.
Therefore, if you decide to disable signal handling all together you *must*
ensure that you at the very least catch signal.SIGTERM and signal.SIGINT with
the ability to call app.close().  You will likely find that it is more
complex than you might think.  The reason we put these mechanisms in place is
primarily that we found it was the best way to a) handle a signal, and b) have
access to our 'app' object in order to be able to call 'app.close()' when a
process is terminated.

Signals Caught by Default
-------------------------

By default Cement catches the signals SIGTERM and SIGINT.  When these signals
are caught, Cement raises the exception 'CaughtSignal(signum, frame)'
where 'signum' and 'frame' are the parameters passed to the signal handler.
By raising an exception, we are able to pass runtime back to our applications
main process (within a try/except block) and maintain the ability to access
our 'application' object without using global objects.

A basic application using default handling might look like:

.. code-block:: python

    import signal
    from cement.core.foundation import CementApp
    from cement.core.exc import CaughtSignal

    with CementApp('myapp') as app:
        try:
            app.run()
        except CaughtSignal as e:
            # do something with e.signum or e.frame (passed from signal)
            if e.signum == signal.SIGTERM:
                print("Caught SIGTERM...")
            elif e.signum == signal.SIGINT:
                print("Caught SIGINT...")


The above provides a very simple means of handling the most common
signals, which in turns allowes our application to "exit clean" by running
``app.close()`` and any ``pre_close`` or ``post_close`` hooks.  If we don't
catch the signals, then the exceptions will be unhandled and the application
will not exit clean.


Using The Signal Hook
---------------------

An alternative way of adding multiple callbacks to a signal handler is by
using the Cement signal hook.  This hook is called anytime a handled signal
is encountered.

.. code-block:: python

    import signal
    from cement.core.foundation import CementApp
    from cement.core.exc import CaughtSignal
    from cement.core import hook

    def my_signal_handler(signum, frame):
        if signum == signal.SIGTERM:
            print("Caught SIGTERM...")
        elif signum == signal.SIGINT:
            print("Caught SIGINT...")

    with CementApp('myapp') as app:
        hook.register('signal', my_signal_handler)
        app.run()


The key thing to note here is that the main application itself handles the
``CaughtSignal`` exception, where as using the cement ``signal`` hook is
useful for plugins and extensions to be able to tie into the signal handling
outside of the main application.  Both serve the same purpose however the
application object is not available (passed to) the cement ``signal`` hook
which limits what can be done within the callback function.  For this reason
any extensions or plugins should use the ``pre_close`` hook as much as
possible as it is always run when ``app.close()`` is called and receives the
``app`` object as one of its parameters.


Configuring Which Signals To Catch
----------------------------------

You can define other signals to catch by passing a list of 'catch_signals' to
foundation.CementApp():

.. code-block:: python

    import signal
    from cement.core.foundation import CementApp

    SIGNALS = [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]

    CementApp('myapp', catch_signals=SIGNALS)
    ...


What happens is, Cement iterates over the catch_signals list and adds a
generic handler function (the same) for each signal.  Because the handler
calls the cement 'signal' hook, and then raises an exception which both pass the
'signum' and 'frame' parameters, you are able to handle the logic elsewhere
rather than assigning a unique callback function for every signal.


What If I Don't Like Your Signal Handler Callback?
--------------------------------------------------

If you want more control over what happens when a signal is caught, you are
more than welcome to override the default signal handler callback.  That said,
please be kind and be sure to atleast run the cement 'signal' hook within your
callback.

.. code-block:: python

    import signal
    from cement.core.foundation import CementApp
    from cement.core import hook

    SIGNALS = [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]

    def my_signal_handler(signum, frame):
        print 'Caught signal %s' % signum

        # execute the cement signal hook
        for res in hook.run('signal', signum, frame):
            pass

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            catch_signals = SIGNALS
            signal_handler = my_signal_handler



This Is Stupid, and UnPythonic - How Do I Disable It?
-----------------------------------------------------

To each their own.  If you simply do not want any kind of signal handling
performed, just set ``catch_signals=None``.

.. code-block:: python

    from cement.core.foundation import foundation

    CementApp('myapp', catch_signals=None)
