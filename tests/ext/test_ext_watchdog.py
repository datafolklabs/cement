
import os
from cement.utils.test import TestApp, raises
from cement.ext.ext_watchdog import WatchdogEventHandler
from cement.core.exc import FrameworkError
from cement.utils import fs


class MyEventHandler(WatchdogEventHandler):
    def on_any_event(self, event):
        # do something with the ``event`` object
        raise Exception("The modified path was: %s" % event.src_path)


class WatchdogApp(TestApp):
    class Meta:
        extensions = ['watchdog']


def test_watchdog(tmp):
    with WatchdogApp() as app:
        app.watchdog.add(tmp.dir, event_handler=MyEventHandler)
        app.run()

        # trigger an event
        f = open(fs.join(tmp.dir, 'test.file'), 'w')
        f.write('test data')
        f.close()


def test_watchdog_app_paths(tmp):
    class MyApp(WatchdogApp):
        class Meta:
            watchdog_paths = [
                (tmp.dir),
                (tmp.dir, WatchdogEventHandler)
            ]

    with WatchdogApp() as app:
        app.run()

        # trigger an event
        f = open(fs.join(tmp.dir, 'test.file'), 'w')
        f.write('test data')
        f.close()


def test_watchdog_app_paths_bad_spec(tmp):
    class MyApp(WatchdogApp):
        class Meta:
            watchdog_paths = [
                [tmp.dir, WatchdogEventHandler]
            ]

    with raises(FrameworkError, match="Watchdog path spec must be a tuple"):
        with MyApp():
            pass


def test_watchdog_default_event_handler(tmp):
    with WatchdogApp() as app:
        app.watchdog.add(tmp.dir)
        app.run()


def test_watchdog_bad_path(tmp):
    with WatchdogApp() as app:
        app.watchdog.add(os.path.join(tmp.dir, 'bogus_sub_dir'))
        app.run()


def test_watchdog_hooks(tmp):
    # FIX ME: this is only coverage...
    def test_hook(app):
        app.counter += 1

    with WatchdogApp() as app:
        app.counter = 0
        app.watchdog.add(tmp.dir)
        app.hook.register('watchdog_pre_start', test_hook)
        app.hook.register('watchdog_post_start', test_hook)
        app.hook.register('watchdog_pre_stop', test_hook)
        app.hook.register('watchdog_post_stop', test_hook)
        app.hook.register('watchdog_pre_join', test_hook)
        app.hook.register('watchdog_post_join', test_hook)
        app.run()

    # yup, the function was run 6 times (once for each hook)
    assert app.counter == 6
