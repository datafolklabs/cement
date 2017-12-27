
import os
from pytest import raises

from cement.core.foundation import TestApp
from cement.core.exc import FrameworkError
from cement.core.output import OutputHandlerBase, OutputHandler, TemplateOutputHandler


### module tests

class TestOutputHandlerBase(object):
    def test_interface(self):
        assert OutputHandlerBase.Meta.interface == 'output'


class TestOutputHandler(object):
    def test_subclassing(self):
        class MyOutputHandler(OutputHandler):
            class Meta:
                label = 'my_output_handler'

            def render(self, *args, **kw):
                pass


        h = MyOutputHandler()
        assert h._meta.interface == 'output'
        assert h._meta.label == 'my_output_handler'


class TestTemplateOutputHandler(object):
    def test_subclassing(self):
        class MyTemplateOutputHandler(TemplateOutputHandler):
            class Meta:
                label = 'my_template_output_handler'

            def render(self, *args, **kw):
                pass


        h = MyTemplateOutputHandler()
        assert h._meta.interface == 'output'
        assert h._meta.label == 'my_template_output_handler'


### app functionality and coverage tests

TEST_TEMPLATE = "%(foo)s"


class MyOutputHandler(TemplateOutputHandler):

    class Meta:
        label = 'my_output_handler'

    def render(self, data, template):
        content = self.load_template(template)
        return content % data


def test_load_template_from_file(tmp):
    template = os.path.join(tmp.dir, 'mytemplate.txt')

    f = open(template, 'w')
    f.write(TEST_TEMPLATE)
    f.close()

    class MyApp(TestApp):
        class Meta:
            template_dir = tmp.dir
            output_handler = MyOutputHandler

    with MyApp() as app:
        app.run()
        assert app.render({'foo' : 'bar'}, 'mytemplate.txt') == 'bar'

        # try and render a missing template
        with raises(FrameworkError, match='Could not locate template: .*'):
            app.render({'foo' : 'bar'}, 'missing-template.txt')
