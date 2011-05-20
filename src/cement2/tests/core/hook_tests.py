"""Tests for cement.core.hook."""

import sys
from nose.tools import with_setup, ok_, eq_, raises
from nose import SkipTest

from cement.core import exc
from cement.core import hook
    

hook.define('cement_test_hook')

def test_define():
    ok_(hook.hooks.has_key('cement_test_hook'))

@raises(exc.CementRuntimeError)
def test_define_again():
    try:
        hook.define('cement_test_hook')
    except exc.CementRuntimeError, e:
        eq_(e.msg, "Hook name 'cement_test_hook' already defined!")
        raise

@hook.register(name='cement_test_hook', weight=99)
def cement_hook_one(*args, **kw):
    return 'kapla 1'

@hook.register(name='cement_test_hook', weight=-1)
def cement_hook_two(*args, **kw):
    return 'kapla 2'
    
@hook.register(name='some_bogus_hook', weight=-1)
def cement_hook_three(*args, **kw):
    return 'kapla 2'
    
def test_bogus_hook_name_on_register():
    eq_(len(hook.hooks['cement_test_hook']), 2)
    
def test_run():
    results = []
    for res in hook.run('cement_test_hook'):
        results.append(res)
    eq_(results[0], 'kapla 2')
    eq_(results[1], 'kapla 1')

@raises(exc.CementRuntimeError)
def test_run_bad_hook():
    for res in hook.run('some_bogus_hook'):
        pass
        

