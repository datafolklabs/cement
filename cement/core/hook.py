"""Cement core hooks module."""

import operator
from ..core import backend, exc

LOG = backend.minimal_logger(__name__)

def define(name):
    """
    Define a hook namespace that plugins can register hooks in.
    
    Required arguments:
    
        name
            The name of the hook, stored as hooks['name']
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core import hook
        
        hook.define('myhookname_hook')
    
    """
    LOG.debug("defining hook '%s'", name)
    if name in backend.hooks:
        raise exc.CementRuntimeError("Hook name '%s' already defined!" % name)
    backend.hooks[name] = []
 
def defined(hook_name):
    """
    Test whether a hook name is defined.
    
    Required Arguments:
    
        hook_type
            The name of the hook (I.e. 'my_hook_does_awesome_things').
    
    Returns: bool
    
    """
    if hook_name in backend.hooks:
        return True
    else:
        return False   
    
def register(name, func, weight=0):
    """
    Register a function to a hook.  The function will be called, in order of
    weight, when the hook is run.

    Required Arguments:
    
        name
            The name of the hook to register too.  I.e. 'pre_setup', 
            'post_run', etc.

        func
            The function to register to the hook.  This is an 
            *un-instantiated*, non-instance method, simple function.
            
    Optional keyword arguments:
    
        weight
            The weight in which to order the hook function (default: 0)
        

    Usage:
    
    .. code-block:: python
        
        from cement.core import hook
        
        def my_hook(*args, **kwargs):
            # do something here
            res = 'Something to return'
            return res
    
        hook.register('post_setup', my_hook)
        
    """
    if name not in backend.hooks:
        LOG.debug("hook name '%s' is not defined!" % name)
        return False
        
    LOG.debug("registering hook '%s' from %s into hooks['%s']" % \
        (func.__name__, func.__module__, name))
    
    # Hooks are as follows: (weight, name, func)
    backend.hooks[name].append((int(weight), func.__name__, func))
    
def run(name, *args, **kwargs):
    """
    Run all defined hooks in the namespace.  Yields the result of each hook
    function run.
    
    Optional arguments:
    
        name
            The name of the hook function
        args
            Any additional args are passed to the hook function
        kwargs
            Any kwargs are passed to the hook function
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core import hook
        
        for result in hook.run('hook_name'):
            # do something with result from each hook function
            ...
    """
    if name not in backend.hooks:
        raise exc.CementRuntimeError("Hook name '%s' is not defined!" % name)

    # Will order based on weight (the first item in the tuple)
    backend.hooks[name].sort(key=operator.itemgetter(0)) 
    for hook in backend.hooks[name]:
        LOG.debug("running hook '%s' (%s) from %s" % (name, hook[2], hook[2].__module__))
        res = hook[2](*args, **kwargs)
        
        # Results are yielded, so you must fun a for loop on it, you can not
        # simply call run_hooks().  
        yield res