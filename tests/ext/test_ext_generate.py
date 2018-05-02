
import os
import re
from cement import TestApp, Controller
from cement.utils.test import raises


def exists_join(*paths):
    return os.path.exists(os.path.join(*paths))


class GenerateBase(Controller):
    class Meta:
        label = 'base'


class GenerateApp(TestApp):
    class Meta:
        extensions = ['jinja2', 'yaml', 'generate', 'alarm']
        template_handler = 'jinja2'
        template_module = 'tests.data.templates'
        handlers = [GenerateBase]


def test_generate(tmp):
    argv = ['generate', 'test1', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        # should have everything
        assert exists_join(tmp.dir, 'take-me')
        res = open(os.path.join(tmp.dir, 'take-me'), 'r').read()
        assert res.find('bar1')
        assert res.find('bar2')
        assert res.find('BAR3')
        assert res.find('Bar4')
        assert res.find('bar5')
        assert res.find('bar6')

        # copied but not rendered
        assert exists_join(tmp.dir, 'exclude-me')
        res = open(os.path.join(tmp.dir, 'exclude-me'), 'r').read()
        assert re.match('.*foo1 => \{\{ foo1 \}\}.*', res)

        # should not have been copied
        assert not exists_join(tmp.dir, 'ignore-me')


def test_prompt(tmp):
    argv = ['generate', 'test1', tmp.dir]

    with GenerateApp(argv=argv) as app:
        msg = "reading from stdin while output is captured"
        with raises(OSError, message=msg):
            app.run()


def test_invalid_case(tmp):
    argv = ['generate', 'test1', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()


def test_invalid_variable_value(tmp):
    argv = ['generate', 'test2', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        msg = "Invalid Response (must match: '.*not-bar1.*')"
        with raises(AssertionError, message=msg):
            app.run()


# additional tests for coverage

def test_no_default(tmp):
    argv = ['generate', 'test3', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        # msg = "Invalid Response (must match: '.*not-bar1.*')"
        # with raises(AssertionError, message=msg):
        app.run()
