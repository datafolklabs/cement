"""Methods and classes to handle Cement Hook support."""

from cement import hooks
from cement.core.exc import CementRuntimeError
from cement.core.log import get_logger

log = get_logger(__name__)

def define_hook(name):
    """
    Define a hook namespace that plugins can register hooks in.
    
    Required arguments:
    
        name
            The name of the hook, stored as hooks['name']
    
    
    Usage:
    
    .. code-block:: python
    
        from cement.core.hook import define_hook
        
        define_hook('myhookname_hook')
        
    """
    log.debug("defining hook '%s'", name)
    if hooks.has_key(name):
        raise CementRuntimeError, "Hook name '%s' already defined!" % name
    hooks[name] = []
    
    
def register_hook(**kwargs):
    """
    Decorator function for plugins to register hooks.  Used as:
    
    Optional keyword arguments:
    
        weight
            The weight in which to order the hook function (default: 0)
    
    Usage:
    
    .. code-block:: python
        
        from cement.core.hook import register_hook
        
        @register_hook()
        def my_hook(*args, **kwargs):
            # do something here
            res = 'Something to return'
            return res
            
    """
    def decorate(func):
        """Decorate the function and add the hook to the global 'hooks'."""
        log.debug("registering hook func '%s' from %s" % \
            (func.__name__, func.__module__))
        if not hooks.has_key(func.__name__):
            log.warn("Hook name '%s' is not define!" % func.__name__)
            return func
        # Hooks are as follows: (wieght, name, func)
        hooks[func.__name__].append(
            (int(kwargs.get('weight', 0)), func.__name__, func)
        )
        return func
    return decorate


def run_hooks(*args, **kwargs):
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
    
        from cement.core.hook import run_hook
        
        for result in run_hooks('hook_name'):
            # do something with result from each hook function
            ...
    """
    name = args[0]
    if not hooks.has_key(name):
        CementRuntimeError, "Hook name '%s' is not defined!" % name
    hooks[name].sort() # Will order based on weight
    for hook in hooks[name]:
        log.debug("running hook '%s' from %s" % (name, hook[2].__module__))
        res = hook[2](*args[1:], **kwargs)
        
        # Results are yielded, so you must fun a for loop on it, you can not
        # simply call run_hooks().  
        yield res