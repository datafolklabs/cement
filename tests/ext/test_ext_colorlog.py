import os
import logging
from tempfile import mkstemp
from cement.core.foundation import TestApp
from cement.ext.ext_colorlog import ColoredFormatter
from cement.utils.misc import init_defaults


_, log_file = mkstemp()
defaults = init_defaults()
defaults['log.colorlog'] = dict(
    file=log_file,
    level='DEBUG',
)


class ColorlogApp(TestApp):
    class Meta:
        config_defaults = defaults
        extensions = ['colorlog']
        log_handler = 'colorlog'


def test_colorlog(caplog):
    META = init_defaults('log.colorlog')
    META['log.colorlog']['propagate'] = True
    with ColorlogApp(meta_defaults=META) as app:
        app.run()
        app.log.info('this is an info message')
        app.log.warning('this is a warning message')
        app.log.error('this is an error message')
        app.log.fatal('this is a fatal message')
        app.log.debug('this is a debug message')
    logged = [log[2] for log in caplog.record_tuples]
    assert 'this is an info message' in logged
    assert 'this is a warning message' in logged
    assert 'this is an error message' in logged
    assert 'this is a debug message' in logged
    assert 'this is a fatal message' in logged


def test_colorize_file_log(tmp):
    # first test with colorize_file_log=true
    log_file = os.path.join(tmp.dir, 'test.log')
    defaults = init_defaults()
    defaults['log.colorlog'] = dict(
        file=log_file,
        level='DEBUG',
        colorize_file_log=True,
    )

    with ColorlogApp(config_defaults=defaults) as app:
        app.run()
        app.log.info('this is an info message')
        klass = app.log._get_file_formatter(app.log._meta.file_format)
        assert isinstance(klass, ColoredFormatter)

    # then test with colorize_file_log=false

    defaults['log.colorlog']['colorize_file_log'] = False

    with ColorlogApp(config_defaults=defaults) as app:
        app.run()
        app.log.info('this is an info message')
        klass = app.log._get_file_formatter(app.log._meta.file_format)
        assert isinstance(klass, logging.Formatter)


def test_colorize_console_log(tmp):
    # first test with colorize_file_log=true
    log_file = os.path.join(tmp.dir, 'test.log')
    defaults = init_defaults()
    defaults['log.colorlog'] = dict(
        file=log_file,
        level='DEBUG',
        colorize_console_log=True,
    )

    with ColorlogApp(config_defaults=defaults) as app:
        app.run()
        app.log.info('this is an info message')
        _format = app.log._meta.console_format
        klass = app.log._get_console_formatter(_format)
        assert isinstance(klass, ColoredFormatter)

    # then test with colorize_file_log=false
    defaults['log.colorlog']['colorize_console_log'] = False

    with ColorlogApp(config_defaults=defaults) as app:
        app.run()
        app.log.info('this is an info message')
        _format = app.log._meta.console_format
        klass = app.log._get_console_formatter(_format)
        assert isinstance(klass, logging.Formatter)
