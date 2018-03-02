
from cement.core.foundation import TestApp
from cement.utils.test import raises
from cement.core.exc import FrameworkError


class MustacheApp(TestApp):
    class Meta:
        extensions = ['mustache']
        output_handler = 'mustache'
        template_module = 'tests.data.templates'
        # template_dirs = []


def test_mustache(rando):
    with MustacheApp() as app:
        res = app.render(dict(foo=rando), 'test_template.mustache')
        mustache_res = "foo equals %s\n" % rando
        assert res == mustache_res


def test_mustache_partials(rando):
    with MustacheApp() as app:
        res = app.render(dict(foo=rando), 'test_base_template.mustache')
        mustache_res = "Inside partial > foo equals %s\n" % rando
        assert res == mustache_res

# derks@20180116: FIXME > Mustache is no longer raising a SyntaxError?

# def test_mustache_bad_template():
#     with MustacheApp() as app:
#         app.render(dict(foo='bar'), 'bad_template.mustache')


def test_mustache_nonexistent_template():
    with MustacheApp() as app:
        msg = "Could not locate template: missing_template.mustache"
        with raises(FrameworkError, match=msg):
            app.render(dict(foo='bar'), 'missing_template.mustache')


def test_mustache_none_template():
    with MustacheApp() as app:
        msg = "Invalid template path 'None'."
        with raises(FrameworkError, match=msg):
            app.render(dict(foo='bar'), None)


def test_mustache_bad_module():
    with MustacheApp() as app:
        msg = "Could not locate template: bad_template.mustache"
        with raises(FrameworkError, match=msg):
            app._meta.template_module = 'this_is_a_bogus_module'
            app.render(dict(foo='bar'), 'bad_template.mustache')
