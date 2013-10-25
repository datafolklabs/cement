"""Tests for cement.utils.misc."""

from cement.utils import test, misc

class BackendTestCase(test.CementCoreTestCase):
    def test_defaults(self):
        defaults = misc.init_defaults('myapp', 'section2', 'section3')
        defaults['myapp']['debug'] = True
        defaults['section2']['foo'] = 'bar'
        self.app = self.make_app('myapp', config_defaults=defaults)
        self.app.setup()
        self.eq(self.app.config.get('myapp', 'debug'), True)
        self.ok(self.app.config.get_section_dict('section2'))

    def test_minimal_logger(self):
        log = misc.minimal_logger(__name__)
        log = misc.minimal_logger(__name__, debug=True)
        log.info('info test')
        log.warn('warn test')
        log.error('error test')
        log.fatal('fatal test')
        log.debug('debug test')

        log.info('info test with namespce', 'test_namespace')

        log.info('info test with extra kwargs', extra=dict(foo='bar'))

        log.info('info test with extra kwargs', extra=dict(namespace='foo'))

        # set logging back to non-debug
        misc.minimal_logger(__name__, debug=False)
        pass

    def test_wrap_str(self):
        text = "aaaaa bbbbb ccccc"
        new_text = misc.wrap(text, width=5)
        parts = new_text.split('\n')
        self.eq(len(parts), 3)
        self.eq(parts[1], 'bbbbb')

        new_text = misc.wrap(text, width=5, indent='***')
        parts = new_text.split('\n')
        self.eq(parts[2], '***ccccc')

    @test.raises(TypeError)
    def test_wrap_int(self):
        text = int('1' * 80)
        try:
            new_text = misc.wrap(text, width=5)
        except TypeError as e:
            self.eq(e.args[0], "`text` must be a string.")
            raise

    @test.raises(TypeError)
    def test_wrap_none(self):
        text = None
        try:
            new_text = misc.wrap(text, width=5)
        except TypeError as e:
            self.eq(e.args[0], "`text` must be a string.")
            raise
