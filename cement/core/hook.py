"""Methods and classes to handle Cement Hook support."""

from cement import hooks
from cement.core.exc import CementRuntimeError
from cement.core.log import get_logger

log = get_logger(__name__)

def define_hook(name):
    """
    Define a hook namespace that plugins can register hooks in.
    """
    log.debug("defining hook '%s'", name)
    if hooks.has_key(name):
        raise CementRuntimeError, "Hook name '%s' already defined!" % name
    hooks[name] = []
    
    
def register_hook(**kwargs):
    """
    Decorator function for plugins to register hooks.  Used as:
    
    @register_hook()
    def my_hook():
        ...
    """
    def decorate(func):
        """Decorate the function and add the hook to the global 'hooks'."""
        log.debug("registering hook func '%s' from %s" % \
            (func.__name__, func.__module__))
        if not hooks.has_key(func.__name__):
            log.warn("Hook name '%s' is not define!" % func.__name__)
            return func
        # (1) is the list of registered hooks in the namespace
        hooks[func.__name__].append(
            (int(kwargs.get('weight', 0)), func.__name__, func)
        )
        return func
    return decorate


def run_hooks(*args, **kwargs):
    """
    Run all defined hooks in the namespace.  Returns a list of return data.
    """
    name = args[0]
    if not hooks.has_key(name):
        CementRuntimeError, "Hook name '%s' is not defined!" % name
    hooks[name].sort() # will order based on weight
    for hook in hooks[name]:
        log.debug("running hook '%s' from %s" % (name, hook[2].__module__))
        res = hook[2](*args[1:], **kwargs)
        
        # FIXME: Need to validate the return data somehow
        yield res