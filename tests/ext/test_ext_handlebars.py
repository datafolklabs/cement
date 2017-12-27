
import pybars
from pytest import raises
from cement.core.exc import FrameworkError
from cement.core.foundation import TestApp


class HandlebarsApp(TestApp):
    class Meta:
        extensions = ['handlebars']
        output_handler = 'handlebars'
        template_module = 'tests.data.templates'
        template_dirs = []
        handlebars_helpers = {}
        handlebars_partials = ['test_partial_template.handlebars']


def test_handlebars(rando):
    with HandlebarsApp() as app:
        res = app.render(dict(foo=rando), 'test_template.handlebars')
        handlebars_res = "foo equals %s\n" % rando
        assert res == handlebars_res


def test_handlebars_partials(rando):
    with HandlebarsApp() as app:
        res = app.render(dict(foo=rando), 'test_base_template.handlebars')
        handlebars_res = "Inside partial > foo equals %s\n" % rando
        assert res == handlebars_res


def test_handlebars_bad_template():
    with HandlebarsApp() as app:
        with raises(pybars._compiler.PybarsError):
            app.render(dict(foo='bar'), 'bad_template.handlebars')


def test_handlebars_nonexistent_template():
    with HandlebarsApp() as app:
        msg = 'Could not locate template: missing_template.handlebars'
        with raises(FrameworkError, match=msg):
            app.render(dict(foo='bar'), 'missing_template.handlebars')


def test_handlebars_none_template():
    with HandlebarsApp() as app:
        with raises(FrameworkError, match="Invalid template path 'None'."):
            app.render(dict(foo='bar'), None)


def test_handlebars_bad_module():
    with HandlebarsApp() as app:
        msg = "Could not locate template: bad_template.handlebars"
        with raises(FrameworkError, match=msg):
            app._meta.template_module = 'this_is_a_bogus_module'
            app.render(dict(foo='bar'), 'bad_template.handlebars')
