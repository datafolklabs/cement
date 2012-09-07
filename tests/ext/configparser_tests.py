
from cement.utils import test
from cement.core import backend

class ConfigParserConfigHandlerTestCase(test.CementTestCase):
    def test_has_key(self):
        defaults = backend.defaults('test')
        defaults['test']['foo'] = 'bar'
        app = self.make_app(config_defaults=defaults)
        app.setup()
        self.eq(app.config.has_key('test', 'bogus'), False)
        self.eq(app.config.has_key('test', 'foo'), True)
        
        # same thing but ignore deprecation warning
        app = self.make_app(
            config_defaults=defaults, 
            ignore_deprecation_warnings=True
        )
        app.setup()
        self.eq(app.config.has_key('test', 'bogus'), False)