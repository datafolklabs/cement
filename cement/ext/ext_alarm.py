"""
Cement alarm extension module.
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

        Args:
            time (int): The time in seconds to set the alarm to.
            msg (str): The message to display if the alarm is triggered.
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
