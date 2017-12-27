
from pytest import raises
from cement.core.config import ConfigHandlerBase, ConfigHandler


### module tests

class MyConfigHandler(ConfigHandler):
    class Meta:
        label = 'my_config_handler'

    def _parse_file(self, *args, **kw):
        return True

    def parse_files(self, *args, **kw):
        pass

    def keys(self, *args, **kw):
        pass

    def get_sections(self, *args, **kw):
        pass

    def get_section_dict(self, *args, **kw):
        pass

    def add_section(self, *args, **kw):
        pass

    def get(self, *args, **kw):
        pass

    def set(self, *args, **kw):
        pass

    def merge(self, *args, **kw):
        pass

    def has_section(self, *args, **kw):
        pass


class TestConfigHandlerBase(object):
    def test_interface(self):
        assert ConfigHandlerBase.Meta.interface == 'config'


class TestConfigHandler(object):
    def test_subclassing(self):
        h = MyConfigHandler()
        assert h._meta.interface == 'config'
        assert h._meta.label == 'my_config_handler'

    def test_parse_file(self, tmp):
        h = MyConfigHandler()
        assert h.parse_file(tmp.file)
        assert not h.parse_file('/path/to/some/bogus/file')

### app functionality and coverage tests
