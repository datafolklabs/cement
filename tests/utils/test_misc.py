
import os
from pytest import raises

from cement.core.foundation import TestApp
from cement.utils import misc


def test_defaults():
    defaults = misc.init_defaults('section1', 'section2')
    defaults['section1']['debug'] = True
    defaults['section2']['foo'] = 'bar'
    with TestApp(config_defaults=defaults) as app:
        assert app.config.get('section1', 'debug') is True
        assert app.config.get_section_dict('section2') == {'foo': 'bar'}


def test_minimal_logger():
    log = misc.minimal_logger(__name__)
    log = misc.minimal_logger(__name__, debug=True)
    log.info('info test')
    log.warning('warning test')
    log.error('error test')
    log.fatal('fatal test')
    log.debug('debug test')

    log.info('info test with namespce', 'test_namespace')
    log.info('info test with extra kwargs', extra=dict(foo='bar'))
    log.info('info test with extra kwargs', extra=dict(namespace='foo'))

    # set logging back to non-debug
    misc.minimal_logger(__name__, debug=False)

    # coverage ...
    kw = {}
    kw['extra'] = {'namespace': __name__}
    log._get_logging_kwargs(__name__, **kw)

    kw['extra'] = {}
    log._get_logging_kwargs(__name__, **kw)

    os.environ['CEMENT_FRAMEWORK_LOGGING'] = '1'
    log.info('info test')
    log.warning('warning test')
    log.error('error test')
    log.fatal('fatal test')
    log.debug('debug test')


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
