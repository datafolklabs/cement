"""Tests for cement.core.output."""

import os
from tempfile import mkdtemp
from cement.core import exc, backend, output
from cement.utils import test
from cement.utils.misc import init_defaults, rando

APP = rando()[:12]


class TestOutputHandler(output.TemplateOutputHandler):

    class Meta:
        label = 'test_output_handler'

    def render(self, data, template):
        content = self.load_template(template)
        return content % data

TEST_TEMPLATE = "%(foo)s"


class OutputTestCase(test.CementCoreTestCase):

    def setUp(self):
        self.app = self.make_app()

    def test_load_template_from_file(self):
        tmpdir = mkdtemp()
        template = os.path.join(tmpdir, 'mytemplate.txt')

        f = open(template, 'w')
        f.write(TEST_TEMPLATE)
        f.close()

        app = self.make_app(APP,
                            config_files=[],
                            template_dir=tmpdir,
                            output_handler=TestOutputHandler,
                            )
        app.setup()
        app.run()
        self.ok(app.render(dict(foo='bar'), 'mytemplate.txt'))

    @test.raises(exc.FrameworkError)
    def test_load_template_from_bad_file(self):
        tmpdir = mkdtemp()
        template = os.path.join(tmpdir, 'my-bogus-template.txt')

        app = self.make_app(APP,
                            config_files=[],
                            template_dir=tmpdir,
                            output_handler=TestOutputHandler,
                            )
        app.setup()
        app.run()
        app.render(dict(foo='bar'), 'my-bogus-template.txt')
