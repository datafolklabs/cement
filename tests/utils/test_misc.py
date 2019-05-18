
# import os
from pytest import raises
from unittest.mock import patch, PropertyMock
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
