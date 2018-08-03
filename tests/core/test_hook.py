"""Tests for cement.core.hook."""

from unittest.mock import Mock
from pytest import raises
from cement.core.exc import FrameworkError
from cement.core.foundation import TestApp


# module tests

class TestHookManager(object):
    pass


# app functionality and coverage tests

def test_define():
    with TestApp() as app:
        app.hook.define('test_hook')

        # is it defined?
        assert app.hook.defined('test_hook')

        # registering again should throw exception
        with raises(FrameworkError, match='Hook name .* already defined!'):
            app.hook.define('test_hook')


def test_register_and_run():
    def hook_one():
        return 'kapla 1'

    def hook_two():
        return 'kapla 2'

    def hook_three():
        return 'kapla 3'

    with TestApp() as app:
        app.hook.define('test_hook')
        app.hook.register('test_hook', hook_one, weight=99)
        app.hook.register('test_hook', hook_two, weight=-1)
        app.hook.register('test_hook', hook_three, weight=-99)

        assert len(app.hook.__hooks__['test_hook']) == 3

        # and run it... track results to verify weight run order

        results = []
        for res in app.hook.run('test_hook'):
            results.append(res)

        assert results == ['kapla 3', 'kapla 2', 'kapla 1']


def test_register_hook_name_not_defined():
    with TestApp() as app:
        ret = app.hook.register('bogus_hook', print)
        assert ret is False


def test_run_bad_hook():
    with TestApp() as app:
        with raises(FrameworkError, match='Hook name .* is not defined!'):
            for res in app.hook.run('some_bogus_hook'):
                pass


def test_framework_hooks():
    test_hook = Mock(return_value='bogus')
    test_hook.__name__ = 'bogusname'
    test_hook_again = Mock(return_value='fake')
    test_hook_again.__name__ = 'bogusname'

    class MyApp(TestApp):
        class Meta:
            hooks = [
                ('pre_setup', test_hook),
                ('post_setup', test_hook),
                ('pre_run', test_hook),
                ('post_run', test_hook),
                ('pre_argument_parsing', test_hook),
                ('post_argument_parsing', test_hook),
                ('pre_close', test_hook),
                ('post_close', test_hook),
                ('signal', test_hook),
                ('pre_render', test_hook),
                ('pre_render', test_hook_again),
                ('post_render', test_hook),
                ('post_render', test_hook),
            ]

    with MyApp() as app:
        # Pre- and post- setup
        assert test_hook.call_count == 2
        test_hook.reset_mock()

        # Pre/post run (+ pre/post argparse)
        # App has no controller, so it also parses args here
        app.run()
        assert test_hook.call_count == 4
        test_hook.reset_mock()

        # pre/post render
        # two hooks each, one is test_hook_again
        app.render({1: 'bogus'})
        assert test_hook.call_count == 3
        assert test_hook_again.call_count == 1
        test_hook.reset_mock()
        test_hook_again.reset_mock()

        # TODO: Test that signal hook gets called properly

    # pre/post close
    assert test_hook.call_count == 2


def test_generate_type_hook():
    def my_generator():
        for i in [1, 1, 1]:
            yield i

    with TestApp() as app:
        app.hook.define('test_hook')
        app.hook.register('test_hook', my_generator)
        app.run()
        for res in app.hook.run('test_hook'):
            assert res == 1


def test_list():
    with TestApp() as app:
        assert 'pre_setup' in app.hook.list()
