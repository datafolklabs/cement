import os
import shutil
import logging
from pytest import raises
from cement.core.foundation import TestApp
from cement.ext.ext_logging import LoggingLogHandler
from cement.utils.misc import init_defaults


class MyLog(LoggingLogHandler):

    class Meta:
        label = 'mylog'
        level = 'INFO'

    def __init__(self, *args, **kw):
        super(MyLog, self).__init__(*args, **kw)


def test_alternate_namespaces(tmp):
    log_file = os.path.join(tmp.dir, 'test.log')
    defaults = init_defaults('log.logging')
    defaults['log.logging']['to_console'] = False
    defaults['log.logging']['file'] = log_file
    defaults['log.logging']['level'] = 'debug'

    with TestApp(config_defaults=defaults) as app:
        app.log.info('TEST', extra=dict(namespace=__name__))
        app.log.warning('TEST', extra=dict(namespace=__name__))
        app.log.error('TEST', extra=dict(namespace=__name__))
        app.log.critical('TEST', extra=dict(namespace=__name__))
        app.log.fatal('TEST', extra=dict(namespace=__name__))
        app.log.debug('TEST', extra=dict(namespace=__name__))

        app.log.info('TEST', __name__, extra=dict(foo='bar'))
        app.log.warning('TEST', __name__, extra=dict(foo='bar'))
        app.log.error('TEST', __name__, extra=dict(foo='bar'))
        app.log.critical('TEST', __name__, extra=dict(foo='bar'))
        app.log.fatal('TEST', __name__, extra=dict(foo='bar'))
        app.log.debug('TEST', __name__, extra=dict(foo='bar'))

        app.log.info('TEST', __name__)
        app.log.warning('TEST', __name__)
        app.log.error('TEST', __name__)
        app.log.critical('TEST', __name__)
        app.log.fatal('TEST', __name__)
        app.log.debug('TEST', __name__)

    assert os.path.exists(log_file)
    with open(log_file, 'r') as f:
        logs = f.readlines()
        for log in logs:
            assert __name__ in log


def test_bad_level():
    defaults = init_defaults()
    defaults['log.logging'] = dict(
        level='BOGUS',
        to_console=False,
    )

    with TestApp(config_defaults=defaults) as app:
        assert app.log.get_level() == 'INFO'


def test_clear_loggers():
    with TestApp() as app:
        label = app._meta.label
        han = app.handler.get('log', 'logging')
        Log = han()
        Log.clear_loggers(label)

        handler = logging.getLogger("cement:app:%s" % label).handlers
        # Nullhandler remains
        assert len(handler) == 1
        assert isinstance(handler[0], logging.NullHandler)


def test_clear_loggers_via_keyword():
    with TestApp() as app:
        label = app._meta.label
        han = logging.getLogger("cement:app:%s" % label).handlers
        MyLog = LoggingLogHandler(clear_loggers=["%s:%s" % (label, label)])
        MyLog._setup(app)
        assert len(han) == 1
        assert isinstance(han[0], logging.NullHandler)


def test_rotate(tmp):
    log_file = os.path.join(tmp.dir, 'test.log')
    defaults = init_defaults('log.logging')
    defaults['log.logging'] = dict(
        file=log_file,
        level='DEBUG',
        rotate=True,
        max_bytes=10,
        max_files=2,
    )

    with TestApp(config_defaults=defaults) as app:
        app.log.info('test log message')
        app.log.info('test log message 2')
        app.log.info('test log message 3')
        app.log.info('test log message 4')

        # check that a second file was created, because this log is over 12
        # bytes.
        assert os.path.exists("%s.1" % log_file)
        assert os.path.exists("%s.2" % log_file)

        # this file should exist because of max files
        assert os.path.exists("%s.3" % log_file) is False


def test_missing_log_dir(tmp):
    if os.path.exists(tmp.dir):
        shutil.rmtree(tmp.dir)

    defaults = init_defaults('log.logging')
    defaults['log.logging'] = dict(
        file=os.path.join(tmp.dir, 'test.log'),
    )

    # extension generates the dir if it is missing
    with TestApp(config_defaults=defaults):
        assert os.path.exists(tmp.dir)


def test_log_level_argument():
    meta = init_defaults('log.logging')
    meta['log.logging']['log_level_argument'] = ['-l', '--level']
    with TestApp(meta_defaults=meta, argv=['--level', 'debug']) as app:
        app.run()
        assert app.debug is True
        assert app.log.get_level() == 'DEBUG'

    # again without the argument (disabled by default)
    with raises(SystemExit):
        with TestApp(argv=['-l', 'debug']) as app:
            app.run()
