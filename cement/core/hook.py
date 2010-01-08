
from cement import namespaces, hooks
from cement.core.exc import CementRuntimeError
from cement.core.log import get_logger

log = get_logger(__name__)

def define_hook(hook_name):
    """
    Define a hook namespace that plugins can register hooks in.
    """
    if hooks.has_key(hook_name):
        raise CementRuntimeError, "Hook name '%s' already defined!" % hook_name
    hooks[hook_name] = []
    
    
def register_hook(**kwargs):
    """
    Decorator function for plugins to register hooks.  Used as:
    
    @register_hook()
    def my_hook():
        ...
    """
    def decorate(func):
        if not hooks.has_key(func.__name__):
            #raise CementRuntimeError, "Hook name '%s' is not define!" % func.__name__
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
    hook_name = args[0]
    if not hooks.has_key(hook_name):
        CementRuntimeError, "Hook name '%s' is not defined!" % hook_name
    hooks[hook_name].sort() # will order based on weight
    for hook in hooks[hook_name]:
        res = hook[2](*args[1:], **kwargs)
        
        # FIXME: Need to validate the return data somehow
        yield res