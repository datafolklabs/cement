"""
Cement core log module.

"""

from cement2.core import exc, backend, interface, meta
            
def log_validator(klass, obj):
    """Validates an handler implementation against the ILog interface."""
    
    members = [
        'setup',
        'clear_loggers',
        'set_level',
        'level',
        'info', 
        'warn',
        'error', 
        'fatal', 
        'debug', 
        ]
    interface.validate(ILog, obj, members)        
                
class ILog(interface.Interface):
    """
    This class defines the Log Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
        
    Implementations do *not* subclass from interfaces.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import log
        
        class MyLogHandler(object):
            class Meta:
                interface = log.ILog
                label = 'my_log_handler'
            ...
            
    """
    class IMeta:
        label = 'log'
        validator = log_validator
    
    # Must be provided by the implementation
    Meta = interface.Attribute('Handler Meta-data')
    
    def setup(config_obj):
        """
        The setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the :ref:`IConfig` <cement2.core.config>` 
                interface and not a config dictionary, though some config 
                handler implementations may also function like a dict 
                (i.e. configobj).
                
        Returns: n/a
        
        """
        
    def clear_loggers():
        """
        Clear all existing loggers.
        
        """
        
    def set_level(self):
        """
        Set the log level.  Must except one of: 'INFO', 'WARN', 'ERROR', 
        'DEBUG', or 'FATAL'.
        
        """
        
    def level(self):
        """
        Return a string representation of the log level.
        """
    
    def info(self, msg):
        """
        Log to the 'INFO' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
        
    def warn(self, msg):
        """
        Log to the 'WARN' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
    
    def error(self, msg):
        """
        Log to the 'ERROR' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
    
    def fatal(self, msg):
        """
        Log to the 'FATAL' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """
    
    def debug(self, msg):
        """
        Log to the 'DEBUG' facility.
        
        Required Arguments:
        
            msg
                The message to log.
        
        """

class CementLogHandler(meta.MetaMixin):
    def __init__(self, *args, **kw):
        super(CementLogHandler, self).__init__(*args, **kw)
