"""Tests for cement.core.hook."""

import signal
import unittest
from nose.tools import ok_, eq_, raises
from cement2.core import exc, backend, hook, foundation
from cement2 import test_helper as _t


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
    
class HookTestCase(unittest.TestCase):
    def setUp(self):
        self.app = _t.prep()
        hook.define('nosetests_hook')
        
    def test_define(self):
        ok_('nosetests_hook' in backend.hooks)

    @raises(exc.CementRuntimeError)
    def test_define_again(self):
        try:
            hook.define('nosetests_hook')
        except exc.CementRuntimeError as e:
            eq_(e.msg, "Hook name 'nosetests_hook' already defined!")
            raise
    
    def test_hooks_registered(self):
        hook.register(name='nosetests_hook', weight=99)(cement_hook_one)
        hook.register(name='nosetests_hook', weight=-1)(cement_hook_two)
        hook.register(name='some_bogus_hook', weight=-99)(cement_hook_three)
        hook.register()(nosetests_hook)
        eq_(len(backend.hooks['nosetests_hook']), 3)
    
    def test_run(self):
        hook.register(name='nosetests_hook', weight=99)(cement_hook_one)
        hook.register(name='nosetests_hook', weight=-1)(cement_hook_two)
        hook.register(name='nosetests_hook', weight=-99)(cement_hook_three)
        
        results = []
        for res in hook.run('nosetests_hook'):
            results.append(res)
    
        eq_(results[0], 'kapla 3')
        eq_(results[1], 'kapla 2')
        eq_(results[2], 'kapla 1')

    @raises(exc.CementRuntimeError)
    def test_run_bad_hook(self):
        for res in hook.run('some_bogus_hook'):
            pass

    def test_hook_is_defined(self):
        ok_(hook.defined('nosetests_hook'))
        eq_(hook.defined('some_bogus_hook'), False)
        
    def test_framework_hooks(self):
        app = _t.prep('myapp', argv=['--quiet'])
        hook.register(name='cement_pre_setup_hook')(cement_hook_one)
        hook.register(name='cement_post_setup_hook')(cement_hook_one)
        hook.register(name='cement_pre_run_hook')(cement_hook_one)
        hook.register(name='cement_post_run_hook')(cement_hook_one)
        hook.register(name='cement_on_close_hook')(cement_hook_one)
        hook.register(name='cement_signal_hook')(cement_hook_one)
        hook.register(name='cement_pre_render_hook')(cement_hook_one)
        hook.register(name='cement_pre_render_hook')(cement_hook_five)
        hook.register(name='cement_post_render_hook')(cement_hook_one)
        hook.register(name='cement_post_render_hook')(cement_hook_five)
        app.setup()
        app.run()
        app.render(dict(foo='bar'))
        app.close()
    
        # this is where cement_signal_hook is run
        try:
            foundation.cement_signal_handler(signal.SIGTERM, 5)
        except exc.CementSignalError as e:
            pass
