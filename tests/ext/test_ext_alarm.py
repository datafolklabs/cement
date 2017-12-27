
import time
import signal
from pytest import raises
from mock import Mock
from cement.core.exc import CaughtSignal
from cement.core.foundation import TestApp


class AlarmApp(TestApp):
    class Meta:
        extensions = ['alarm']


def test_alarm_timeout():
    with AlarmApp() as app:
        with raises(CaughtSignal) as e:
            app.alarm.set(1, "The Timer Works!")
            time.sleep(3)

        assert e.value.signum == signal.SIGALRM

        # derks@2018-01-15: I think pytest is interrupting cement handling the
        # signal here, so we'll run the hooks manuall
        for res in app.hook.run('signal', app, e.value.signum, e.value.frame):
            pass


def test_alarm_no_timeout():
    with AlarmApp() as app:
        app.alarm.set(3, "The Timer Works!")
        time.sleep(1)
        app.alarm.stop()
