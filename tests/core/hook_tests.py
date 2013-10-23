"""Tests for cement.core.hook."""

import signal
from cement.core import exc, backend, hook, foundation
from cement.utils import test

def cement_hook_one(*args, **kw):
    return 'kapla 1'

def cement_hook_two(*args, **kw):
    return 'kapla 2'

def cement_hook_three(*args, **kw):
    return 'kapla 3'

def nosetests_hook(*args, **kw):
    return 'kapla 4'

def cement_hook_five(app, data):
    return data
    
class HookTestCase(test.CementCoreTestCase):
    def setUp(self):
        self.app = self.make_app()
        hook.define('nosetests_hook')
        
    def test_define(self):
        self.ok('nosetests_hook' in backend.__hooks__)

    @test.raises(exc.FrameworkError)
    def test_define_again(self):
        try:
            hook.define('nosetests_hook')
        except exc.FrameworkError as e:
            self.eq(e.msg, "Hook name 'nosetests_hook' already defined!")
            raise
    
    def test_hooks_registered(self):
        hook.register('nosetests_hook', cement_hook_one, weight=99)
        hook.register('nosetests_hook', cement_hook_two, weight=-1)
        hook.register('some_bogus_hook', cement_hook_three, weight=-99)
        self.eq(len(backend.__hooks__['nosetests_hook']), 2)
    
    def test_run(self):
        hook.register('nosetests_hook', cement_hook_one, weight=99)
        hook.register('nosetests_hook', cement_hook_two, weight=-1)
        hook.register('nosetests_hook', cement_hook_three, weight=-99)
        
        results = []
        for res in hook.run('nosetests_hook'):
            results.append(res)
    
        self.eq(results[0], 'kapla 3')
        self.eq(results[1], 'kapla 2')
        self.eq(results[2], 'kapla 1')

    @test.raises(exc.FrameworkError)
    def test_run_bad_hook(self):
        for res in hook.run('some_bogus_hook'):
            pass

    def test_hook_is_defined(self):
        self.ok(hook.defined('nosetests_hook'))
        self.eq(hook.defined('some_bogus_hook'), False)
        
    def test_framework_hooks(self):
        app = self.make_app('myapp', argv=['--quiet'])
        hook.register('pre_setup', cement_hook_one)
        hook.register('post_setup', cement_hook_one)
        hook.register('pre_run', cement_hook_one)
        hook.register('post_run', cement_hook_one)
        hook.register('pre_argument_parsing', cement_hook_one)
        hook.register('post_argument_parsing', cement_hook_one)
        hook.register('pre_close', cement_hook_one)
        hook.register('post_close', cement_hook_one)
        hook.register('signal', cement_hook_one)
        hook.register('pre_render', cement_hook_one)
        hook.register('pre_render', cement_hook_five)
        hook.register('post_render', cement_hook_one)
        hook.register('post_render', cement_hook_five)
        app.setup()
        app.run()
        app.render(dict(foo='bar'))
        app.close()
    
        # this is where cement_signal_hook is run
        try:
            foundation.cement_signal_handler(signal.SIGTERM, 5)
        except exc.CaughtSignal as e:
            pass
