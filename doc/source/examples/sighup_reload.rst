Reload Application on SIGHUP
============================

A common convention in the Linux world is to handle a ``SIGHUP`` signal, by
reloading the current runtime within the same process ID (``pid``).  The 
following example demonstrates how you might achieve that:

.. code-block:: python

    import signal
    from time import sleep
    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose
    from cement.core.exc import CaughtSignal


    class MyController(CementBaseController):
        class Meta:
            label = 'base'

        @expose(hide=True)
        def default(self):
            print('Inside MyController.default()')

            ### inner loop where the application logic happens
            while True:
                print('Inside Inner Loop')
                sleep(5)

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            base_controller = MyController


    with MyApp() as app:
        ### outer loop where signals are handles, and application reload 
        ### happens

        keep_alive = True
        while keep_alive is True:
            try:
                app.run()
            except CaughtSignal as e:
                app.log.warning(e.msg)
                if e.signum in [signal.SIGHUP]:
                    app.log.warning('Reloading MyApp')
                    app.reload()
                    keep_alive = True
                else:
                    app.exit_code = 1
                    keep_alive = False


Running the application shows the inner loop in action:

.. code-block:: console

    $ python myapp.py
    Inside MyController.default()
    Inside Inner Loop
    Inside Inner Loop
    Inside Inner Loop
    Inside Inner Loop
    Inside Inner Loop
    Inside Inner Loop
    Inside Inner Loop


If we grab the PID in another terminal, and send it a SIGHUP signal we can 
see it reload:

.. code-block:: console

    $ ps auxw | grep [m]yapp
    derks            1317   0.0  0.1  2425792  12988 s001  S+   10:03PM   0:00.11 python myapp.py


In the original terminal (running our app) we see that the app reloads and the
inner loop continues:

.. code-block:: console

    Caught signal 1
    WARNING: Reloading myapp
    Inside MyController.default()
    Inside Inner Loop
    Inside Inner Loop


However, the PID remains the same:

.. code-block:: console

    $ ps auxw | grep [m]yapp
    derks            1317   0.0  0.1  2425792  13012 s001  S+   10:03PM   0:00.11 python myapp.py


If you'd like to see even more detail on what Cement is doing during the 
reload try adding ``--debug``.
