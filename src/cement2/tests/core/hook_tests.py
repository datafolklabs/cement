"""Tests for cement.core.hook."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement2.core import exc, backend, hook
    

hook.define('nosetests_hook')

def test_define():
    ok_(backend.hooks.has_key('nosetests_hook'))

@raises(exc.CementRuntimeError)
def test_define_again():
    try:
        hook.define('nosetests_hook')
    except exc.CementRuntimeError, e:
        eq_(e.msg, "Hook name 'nosetests_hook' already defined!")
        raise

@hook.register(name='nosetests_hook', weight=99)
def cement_hook_one(*args, **kw):
    return 'kapla 1'

@hook.register(name='nosetests_hook', weight=-1)
def cement_hook_two(*args, **kw):
    return 'kapla 2'
    
@hook.register(name='some_bogus_hook', weight=-99)
def cement_hook_three(*args, **kw):
    return 'kapla 3'
    
@hook.register()
def nosetests_hook(*args, **kw):
    return 'kapla 4'
    
def test_hooks_registered():
    eq_(len(backend.hooks['nosetests_hook']), 3)
    
def test_run():
    results = []
    for res in hook.run('nosetests_hook'):
        results.append(res)
    eq_(results[0], 'kapla 2')
    eq_(results[1], 'kapla 4')
    eq_(results[2], 'kapla 1')

@raises(exc.CementRuntimeError)
def test_run_bad_hook():
    for res in hook.run('some_bogus_hook'):
        pass
        

