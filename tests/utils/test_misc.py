
# import os
import logging
from unittest.mock import PropertyMock, patch

from pytest import raises

from cement.core.foundation import TestApp
from cement.utils import misc


def test_is_true():
    # true
    assert misc.is_true(1)
    assert misc.is_true('1')
    assert misc.is_true('true')
    assert misc.is_true('True')
    assert misc.is_true('TRUE')
    assert misc.is_true('tRue')
    assert misc.is_true('yes')
    assert misc.is_true('y')
    assert misc.is_true('on')
    assert misc.is_true(True)

    # false
    assert not misc.is_true(0)
    assert not misc.is_true('0')
    assert not misc.is_true('false')
    assert not misc.is_true('False')
    assert not misc.is_true('FALSE')
    assert not misc.is_true('fAlse')
    assert not misc.is_true('no')
    assert not misc.is_true('n')
    assert not misc.is_true('off')
    assert not misc.is_true(False)


def test_defaults():
    defaults = misc.init_defaults('section1', 'section2')
    defaults['section1']['debug'] = True
    defaults['section2']['foo'] = 'bar'
    with TestApp(config_defaults=defaults) as app:
        assert app.config.get('section1', 'debug') is True
        assert app.config.get_section_dict('section2') == {'foo': 'bar'}


def test_minimal_logger_get_kwargs():
    log = misc.minimal_logger(__name__)

    # no keywords
    kw = log._get_logging_kwargs(__name__ + '.bogus')
    assert 'extra' in kw.keys()
    assert kw['extra']['namespace'] == __name__ + '.bogus'

    # keywords with extra
    extra_dict = {'extra': {}}
    kw = log._get_logging_kwargs(__name__ + '.bogus', **extra_dict)
    assert kw['extra']['namespace'] == __name__ + '.bogus'

    # keywords with extra and namespace
    extra_dict = {'extra': {'namespace': __name__ + '.fake'}}
    kw = log._get_logging_kwargs('fake', **extra_dict)
    assert kw['extra']['namespace'] == __name__ + '.fake'


def test_minimal_logger_logging_is_enabled(caplog):
    with patch('cement.utils.misc.MinimalLogger.logging_is_enabled',
               new_callable=PropertyMock) as mock:
        mock.return_value = True

        log = misc.minimal_logger(__name__, True)

        log.info('info test')
        log.warning('warning test')
        log.error('error test')
        log.fatal('fatal test')
        log.debug('debug test')

        assert (__name__, 20, 'info test') in caplog.record_tuples
        assert (__name__, 30, 'warning test') in caplog.record_tuples
        assert (__name__, 40, 'error test') in caplog.record_tuples
        assert (__name__, 50, 'fatal test') in caplog.record_tuples
        assert (__name__, 10, 'debug test') in caplog.record_tuples

        mock.return_value = False
        log.info('do not log this')
        log.warning('do not log this')
        log.error('do not log this')
        log.fatal('do not log this')
        log.debug('do not log this')
        for logged in caplog.record_tuples:
            assert logged[2] != 'do not log this'


def test_minimal_logger_with_arguments(caplog):
    with patch('cement.utils.misc.MinimalLogger.logging_is_enabled',
               new_callable=PropertyMock) as mock:
        log = misc.minimal_logger(__name__)
        mock.return_value = True

        log.info('info test with namespace', 'test_namespace')
        assert caplog.records[0].namespace == 'test_namespace'
        assert caplog.records[0].message == 'info test with namespace'

        log.info('info test with extra kwargs', extra=dict(foo='bar'))
        assert caplog.records[1].foo == 'bar'

        log.info('info test with extra kwargs', extra=dict(namespace='foo'))
        assert caplog.records[2].namespace == 'foo'


def test_wrap_str():
    text = "aaaaa bbbbb ccccc"
    new_text = misc.wrap(text, width=5)
    parts = new_text.split('\n')
    assert len(parts) == 3
    assert parts[1] == 'bbbbb'

    new_text = misc.wrap(text, width=5, indent='***')
    parts = new_text.split('\n')
    assert parts[2] == '***ccccc'


def test_wrap_non_str():
    with raises(TypeError):
        misc.wrap(int('1' * 80), width=5)

    with raises(TypeError):
        misc.wrap(None, width=5)


def test_minimal_logger_does_not_duplicate_handlers():
    # Regression: `logging.getLogger(namespace)` returns the same
    # backend logger instance per name, so calling
    # `minimal_logger(ns)` repeatedly would otherwise stack a fresh
    # `StreamHandler` on each call (every log emit would print
    # multiple times). The MinimalLogger.__init__ idempotency guard
    # only attaches a handler when `self.backend.handlers` is empty.
    ns = 'cement.test.minimal_logger_idempotency'
    backend = logging.getLogger(ns)
    backend.handlers = []  # isolate from any prior test pollution

    misc.minimal_logger(ns)
    assert len(backend.handlers) == 1

    misc.minimal_logger(ns)
    assert len(backend.handlers) == 1


def _file_handlers(backend):
    return [h for h in backend.handlers
            if isinstance(h, logging.FileHandler)]


def test_minimal_logger_framework_log_file(tmp_path, monkeypatch):
    # issue-593: when CEMENT_FRAMEWORK_LOG_FILE is set and framework
    # logging is enabled, framework output is *also* written to the file.
    ns = 'cement.test.framework_log_file'
    backend = logging.getLogger(ns)
    backend.handlers = []  # isolate from any prior test pollution

    log_file = tmp_path / 'framework.log'
    monkeypatch.setenv('CEMENT_LOG', '1')
    monkeypatch.setenv('CEMENT_FRAMEWORK_LOG_FILE', str(log_file))

    log = misc.minimal_logger(ns)
    log.debug('debug to file')

    # exactly one FileHandler on the shared backend
    handlers = _file_handlers(backend)
    assert len(handlers) == 1
    handlers[0].flush()

    contents = log_file.read_text()
    assert 'debug to file' in contents
    assert ns in contents

    backend.handlers = []  # cleanup shared backend state


def test_minimal_logger_no_framework_log_file(monkeypatch):
    # issue-593: env unset => behavior unchanged, no FileHandler attached.
    ns = 'cement.test.framework_log_file_unset'
    backend = logging.getLogger(ns)
    backend.handlers = []

    monkeypatch.delenv('CEMENT_FRAMEWORK_LOG_FILE', raising=False)

    misc.minimal_logger(ns)
    assert _file_handlers(backend) == []

    backend.handlers = []


def test_minimal_logger_framework_log_file_idempotent(tmp_path, monkeypatch):
    # issue-593: repeated calls for the same namespace + path must not
    # stack a duplicate FileHandler (no double-writes).
    ns = 'cement.test.framework_log_file_idempotent'
    backend = logging.getLogger(ns)
    backend.handlers = []

    log_file = tmp_path / 'idempotent.log'
    monkeypatch.setenv('CEMENT_FRAMEWORK_LOG_FILE', str(log_file))

    misc.minimal_logger(ns)
    assert len(_file_handlers(backend)) == 1

    misc.minimal_logger(ns)
    assert len(_file_handlers(backend)) == 1

    backend.handlers = []


def test_minimal_logger_framework_log_file_invalid_path(tmp_path, monkeypatch):
    # issue-593: an invalid/unwritable path (parent dir missing) is
    # silently ignored — no FileHandler attached, no crash, no stderr
    # spam — framework logging is a silent dev aid.
    ns = 'cement.test.framework_log_file_invalid'
    backend = logging.getLogger(ns)
    backend.handlers = []

    bad_path = tmp_path / 'no' / 'such' / 'dir.log'
    monkeypatch.setenv('CEMENT_FRAMEWORK_LOG_FILE', str(bad_path))

    # must not raise
    misc.minimal_logger(ns)
    assert _file_handlers(backend) == []

    backend.handlers = []


def test_minimal_logger_framework_log_file_not_created_until_write(
        tmp_path, monkeypatch):
    # issue-593: setting CEMENT_FRAMEWORK_LOG_FILE without enabling
    # framework logging must NOT create a phantom empty file. delay=True
    # plus the logging_is_enabled emit gate means the file only appears
    # once something is actually logged.
    ns = 'cement.test.framework_log_file_no_phantom'
    backend = logging.getLogger(ns)
    backend.handlers = []

    log_file = tmp_path / 'phantom.log'
    monkeypatch.delenv('CEMENT_LOG', raising=False)
    monkeypatch.delenv('CEMENT_FRAMEWORK_LOGGING', raising=False)
    monkeypatch.setenv('CEMENT_FRAMEWORK_LOG_FILE', str(log_file))

    log = misc.minimal_logger(ns)

    # handler is attached (path is valid + writable) but the file is not
    # opened/created yet (delay=True)
    assert len(_file_handlers(backend)) == 1
    assert not log_file.exists()

    # logging is disabled, so an emit writes nothing and no file appears
    log.debug('should not be written')
    assert not log_file.exists()

    backend.handlers = []
