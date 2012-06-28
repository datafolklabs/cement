"""Cement core hooks module."""

import operator
from ..core import backend, exc

Log = backend.minimal_logger(__name__)

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
    Log.debug("defining hook '%s'", name)
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
    
class register(object):
    """
    Decorator function for plugins to register hooks.
    
    Optional keyword arguments:
    
        weight
            The weight in which to order the hook function (default: 0)
        
        name
            The name of the hook to register too.  If not passed, the __name__
            of the decorated function will be used.

    Usage:
    
    .. code-block:: python
        
        from cement.core import hook
        
        @hook.register()
        def my_hook(*args, **kwargs):
            # do something here
            res = 'Something to return'
            return res
    
    """
    def __init__(self, weight=0, name=None):
        self.weight = weight
        self.name = name

    def __call__(self, func):
        if not self.name:
            self.name = func.__name__

        if self.name not in backend.hooks:
            Log.debug("hook name '%s' is not defined!" % self.name)
            return func
            
        Log.debug("registering hook func '%s' from %s into hooks['%s']" % \
            (func.__name__, func.__module__, self.name))
        # Hooks are as follows: (weight, name, func)
        backend.hooks[self.name].append((int(self.weight), func.__name__, func))
        return func
    
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
        Log.debug("running hook '%s' (%s) from %s" % (name, hook[2], hook[2].__module__))
        res = hook[2](*args, **kwargs)
        
        # Results are yielded, so you must fun a for loop on it, you can not
        # simply call run_hooks().  
        yield res