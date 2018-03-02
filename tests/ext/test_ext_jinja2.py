
import os
import jinja2
from shutil import copyfile
from cement.utils.test import TestApp, raises
from cement.core.exc import FrameworkError
from cement.utils import fs


class Jinja2App(TestApp):
    class Meta:
        extensions = ['jinja2']
        output_handler = 'jinja2'
        template_module = 'tests.data.templates'
        template_dirs = []
        handlebars_helpers = {}


def test_jinja2(rando):
    with Jinja2App() as app:
        res = app.render(dict(foo=rando), 'test_template.jinja2')
        jinja2_res = "foo equals %s\n" % rando
        assert res == jinja2_res


def test_jinja2_utf8(rando):
    with Jinja2App() as app:
        res = app.render(dict(foo=rando), 'test_template_utf8.jinja2')
        jinja2_res = u"foo est égal à %s\n" % rando
        assert res == jinja2_res


def test_jinja2_filesystemloader(tmp, rando):
    with Jinja2App() as app:
        app._meta.template_dirs = [tmp.dir]

        # make sure it doesn't load from the tests directory module regardless
        app._meta.template_module = 'some.bogus.module.path'

        tests_dir = os.path.dirname(os.path.dirname(__file__))

        from_file = fs.join(tests_dir, 'data', 'templates',
                            'test_template_parent.jinja2')
        to_file = fs.join(tmp.dir, 'test_template_parent.jinja2')
        copyfile(from_file, to_file)

        from_file = fs.join(tests_dir, 'data', 'templates',
                            'test_template_child.jinja2')
        to_file = fs.join(tmp.dir, 'test_template_child.jinja2')
        copyfile(from_file, to_file)

        res = app.render(dict(foo=rando), 'test_template_child.jinja2')
        jinja2_res = "foo equals %s\n" % rando
        assert res == jinja2_res


def test_jinja2_packageloader(rando):
    with Jinja2App() as app:
        app._meta.template_module = 'tests.data.templates'
        app._meta.template_dirs = []
        res = app.render(dict(foo=rando), 'test_template_child.jinja2')
        jinja2_res = "foo equals %s\n" % rando
        assert res == jinja2_res


def test_jinja2_bad_template():
    with Jinja2App() as app:
        with raises(jinja2.exceptions.TemplateSyntaxError):
            app.render(dict(foo='bar'), 'bad_template.jinja2')


def test_jinja2_nonexistent_template():
    with Jinja2App() as app:
        msg = "Could not locate template: missing_template.jinja2"
        with raises(FrameworkError, match=msg):
            app.render(dict(foo='bar'), 'missing_template.jinja2')


def test_jinja2_none_template():
    with Jinja2App() as app:
        msg = "Invalid template path 'None'."
        with raises(FrameworkError, match=msg):
            app.render(dict(foo='bar'), None)


def test_jinja2_bad_module():
    with Jinja2App() as app:
        msg = "Could not locate template: bad_template.jinja2"
        with raises(FrameworkError, match=msg):
            app._meta.template_module = 'this_is_a_bogus_module'
            app.render(dict(foo='bar'), 'bad_template.jinja2')
