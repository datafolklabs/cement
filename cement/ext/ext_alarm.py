"""
The Alarm Extension provides easy access to setting an application alarm to
handle timing out operations.  See the
`Python Signal Library <https://docs.python.org/3.5/library/signal.html>`_.

Requirements
------------

 * No external dependencies.
 * Only available on Unix/Linux


Configuration
-------------

This extension does not honor any application configuration settings.


Usage
-----

.. code-block:: python

    import time
    from cement.core.foundation import CementApp
    from cement.core.exc import CaughtSignal


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            exit_on_close = True
            extensions = ['alarm']


    with MyApp() as app:
        try:
            app.run()
            app.alarm.set(3, "The operation timed out after 3 seconds!")

            # do something that takes time to operate
            time.sleep(5)

            app.alarm.stop()

        except CaughtSignal as e:
            print(e.msg)
            app.exit_code = 1

Looks like:

.. code-block:: console

    $ python myapp.py
    ERROR: The operation timed out after 3 seconds!
    Caught signal 14

"""

import signal
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


def alarm_handler(app, signum, frame):
    if signum == signal.SIGALRM:
        app.log.error(app.alarm.msg)


class AlarmManager(object):
    """
    Lets the developer easily set and stop an alarm.  If the
    alarm exceeds the given time it will raise ``signal.SIGALRM``.

    """

    def __init__(self, *args, **kw):
        super(AlarmManager, self).__init__(*args, **kw)
        self.msg = None

    def set(self, time, msg):
        """
        Set the application alarm to ``time`` seconds.  If the time is
        exceeded ``signal.SIGALRM`` is raised.

        :param time: The time in seconds to set the alarm to.
        :param msg: The message to display if the alarm is triggered.
        """

        LOG.debug('setting application alarm for %s seconds' % time)
        self.msg = msg
        signal.alarm(int(time))

    def stop(self):
        """
        Stop the application alarm.
        """
        LOG.debug('stopping application alarm')
        signal.alarm(0)


def load(app):
    app.catch_signal(signal.SIGALRM)
    app.extend('alarm', AlarmManager())
    app.hook.register('signal', alarm_handler)
