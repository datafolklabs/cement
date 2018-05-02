
from cement.core.template import TemplateHandlerBase, TemplateHandler


# module tests

class TestTemplateHandlerBase(object):
    def test_interface(self):
        assert TemplateHandlerBase.Meta.interface == 'template'


class TestTemplateHandler(object):
    def test_subclassing(self):
        class MyTemplateHandler(TemplateHandler):
            class Meta:
                label = 'my_template_handler'

            def render(self, *args, **kw):
                pass

            def copy(self, *args, **kw):
                pass

            def load(self, *args, **kw):
                pass

        h = MyTemplateHandler()
        assert h._meta.interface == 'template'
        assert h._meta.label == 'my_template_handler'


# app functionality and coverage tests
