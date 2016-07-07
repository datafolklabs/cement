"""Tests for cement.ext.ext_alarm."""

import sys
import time
import signal
from cement.core.exc import CaughtSignal
from cement.utils import test


class AlarmExtTestCase(test.CementExtTestCase):

    def setUp(self):
        super(AlarmExtTestCase, self).setUp()
        self.app = self.make_app('tests',
                                 extensions=['alarm'],
                                 argv=[]
                                 )

    @test.raises(CaughtSignal)
    def test_alarm_timeout(self):
        global app
        app = self.app
        with app as app:
            try:
                app.alarm.set(1, "The Timer Works!")
                time.sleep(3)
            except CaughtSignal as e:
                self.eq(e.signum, signal.SIGALRM)
                raise

    def test_alarm_no_timeout(self):
        with self.app as app:
            app.alarm.set(3, "The Timer Works!")
            time.sleep(1)
            app.alarm.stop()
        