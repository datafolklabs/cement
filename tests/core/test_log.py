

from pytest import raises

from cement import init_defaults
from cement.core.foundation import TestApp
from cement.core.log import LogHandlerBase, LogHandler


### module tests

class TestLogHandlerBase(object):
    def test_interface(self):
        assert LogHandlerBase.Meta.interface == 'log'


class TestLogHandler(object):

    def test_subclassing(self):

        class MyLogHandler(LogHandler):

            class Meta:
                label = 'my_log_handler'


            def set_level(self):
                pass


            def get_level(self):
                pass


            def info(self, msg):
                pass


            def warning(self, msg):
                pass


            def error(self, msg):
                pass


            def fatal(self, msg):
                pass


            def debug(self, msg):
                pass

        h = MyLogHandler()
        assert h._meta.interface == 'log'
        assert h._meta.label == 'my_log_handler'


### app functionality and coverage tests


def test_unproviding_handler():

    class BogusHandler(LogHandler):

        class Meta:
            label = 'bogus'

    with TestApp() as app:
        msg = "Can't instantiate abstract class .* with abstract methods"
        with raises(TypeError, match=msg):
            app.handler.register(BogusHandler)


def test_logging():
    defaults = init_defaults()
    defaults['log.logging'] = dict(
        file='/dev/null',
        to_console=True
    )
    with TestApp(config_defaults=defaults) as app:
        app.log.info('Info Message')
        app.log.warning('Warning Message')
        app.log.error('Error Message')
        app.log.fatal('Fatal Message')
        app.log.debug('Debug Message')

        # get level
        assert app.log.get_level() == 'INFO'

        # set level
        app.log.set_level('WARNING')
        assert app.log.get_level() == 'WARNING'

        # set a bad level should default to INFO
        app.log.set_level('BOGUS')
        assert app.log.get_level() == 'INFO'
