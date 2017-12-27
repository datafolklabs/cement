"""Tests for cement.core.hook."""

from pytest import raises

from cement.core.hook import HookManager
from cement.core.exc import FrameworkError
from cement.core.foundation import TestApp


### module tests

class TestHookManager(object):
    pass


### app functionality and coverage tests

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


def test_run_bad_hook():
    with TestApp() as app:
        with raises(FrameworkError, match='Hook name .* is not defined!'):
            for res in app.hook.run('some_bogus_hook'):
                pass


def test_framework_hooks():
    def test_hook(*args, **kw):
        pass

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
                ('pre_render', test_hook),
                ('post_render', test_hook),
                ('post_render', test_hook),
            ]

    with MyApp() as app:
        app.run()
