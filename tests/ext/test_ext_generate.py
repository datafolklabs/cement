import os
import re
from unittest.mock import patch
from cement import TestApp, Controller
from cement.utils import shell
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
        assert res.find('bar1') >= 0
        assert res.find('bar2') >= 0
        assert res.find('BAR3') >= 0
        assert res.find('Bar4') >= 0
        assert res.find('bar5') >= 0
        assert res.find('bar6') >= 0

        # copied but not rendered
        assert exists_join(tmp.dir, 'exclude-me')
        res = open(os.path.join(tmp.dir, 'exclude-me'), 'r').read()
        assert re.match(r'.*foo1 => \{\{ foo1 \}\}.*', res)

        # should not have been copied
        assert not exists_join(tmp.dir, 'ignore-me')

    # test generate again to trigger already exists

    with GenerateApp(argv=argv) as app:
        with raises(AssertionError, match='Destination file already exists'):
            app.run()


def test_prompt(tmp):
    argv = ['generate', 'test1', tmp.dir]

    with GenerateApp(argv=argv) as app:
        msg = "reading from stdin while output is captured"
        with raises(OSError, match=msg):
            app.run()


def test_invalid_case(tmp):
    argv = ['generate', 'test3', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        with open(os.path.join(tmp.dir, 'take-me'), 'r') as f:
            res = f.read()
            # Assert that the case was not modified
            assert 'bar1' in res


def test_invalid_variable_value(tmp):
    argv = ['generate', 'test2', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        msg = "Invalid Response.*"
        with raises(AssertionError, match=msg):
            app.run()


def test_no_default(tmp):
    with patch.object(shell.Prompt, 'prompt', return_value='Bogus'):
        argv = ['generate', 'test5', tmp.dir]

        with GenerateApp(argv=argv) as app:
            app.run()
            with open(os.path.join(tmp.dir, 'take-me'), 'r') as f:
                res = f.read()
                assert 'Bogus' in res


def test_clone(tmp):
    # first test for already exists
    argv = ['generate', 'test1', '--clone', tmp.dir]
    with raises(AssertionError, match='(.*)already exists(.*)'):
        with GenerateApp(argv=argv) as app:
            app.run()

    # then force it
    argv = ['generate', 'test1', '--clone', tmp.dir, '--force']
    with GenerateApp(argv=argv) as app:
        app.run()

    assert exists_join(tmp.dir, '.generate.yml')


def test_generate_from_template_dir(tmp):
    class NoTemplateApp(TestApp):
        class Meta:
            extensions = ['jinja2', 'yaml', 'generate', 'alarm']
            template_handler = 'jinja2'
            template_module = __name__
            handlers = [GenerateBase]

    # should use the templates dir passed as keyword
    # instead of the template_module in the Meta info
    argv = ['generate', 'test1', tmp.dir, '--defaults']
    with NoTemplateApp(argv=argv, template_dir='tests/data/templates') as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        res = open(os.path.join(tmp.dir, 'take-me'), 'r').read()
        assert res.find('bar1') >= 0


def test_generate_default_command(tmp):
    # default command for generate should call print_help
    patch_target = 'cement.ext.ext_argparse.ArgparseArgumentHandler.print_help'
    with patch(patch_target) as mock:
        argv = ['generate']
        with GenerateApp(argv=argv) as app:
            app.run()
    assert mock.call_count == 1


def test_filtered_sub_dirs(tmp):
    tmp.cleanup = False
    argv = ['generate', 'test4', tmp.dir, '--defaults']

    with GenerateApp(argv=argv) as app:
        app.run()

        assert exists_join(tmp.dir, 'take-me')
        assert exists_join(tmp.dir, 'take-me', 'take-me')
        assert exists_join(tmp.dir, 'take-me', 'exclude-me')
        assert not exists_join(tmp.dir, 'take-me', 'ignore-me')
        assert exists_join(tmp.dir, 'exclude-me')
        assert exists_join(tmp.dir, 'exclude-me', 'take-me')
        assert not exists_join(tmp.dir, 'ignore-me')
        assert not exists_join(tmp.dir, 'ignore-me', 'take-me')
