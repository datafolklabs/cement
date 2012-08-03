"""Logging Framework Extension"""

import os
import logging
from ..core import exc, log, handler
from ..utils.misc import is_true

class LoggingLogHandler(log.CementLogHandler):  
    """
    This class is an implementation of the :ref:`ILog <cement.core.log>` 
    interface, and sets up the logging facility using the standard Python
    `logging <http://docs.python.org/library/logging.html>`_ module. 
    
    Configuration Options
    
    The following configuration options are recognized in this class:
    
        <app_label>.debug
        
        log.file
        
        log.to_console
        
        log.rotate
        
        log.max_bytes
        
        log.max_files
    
    
    A sample config section (in any config file) might look like:
    
    .. code-block:: text
    
        [myapp]
        debug = True
        
        [log]
        file = /path/to/config/file
        level = info
        to_console = true
        rotate = true
        max_bytes = 512000
        max_files = 4
        
    """
    class Meta:
        """Handler meta-data."""
        
        interface = log.ILog
        """The interface that this class implements."""
        
        label = 'logging'
        """The string identifier of this handler."""
        
        namespace = None
        """
        The logging namespace.  
        
        Note: Although Meta.namespace defaults to None, Cement will set this 
        to the application label (CementApp.Meta.label) if not set during
        setup.
        """
        
        file_format = "%(asctime)s (%(levelname)s) %(namespace)s : %(message)s"
        """The logging format for the file logger."""
        
        console_format = "%(levelname)s: %(message)s"
        """The logging format for the consoler logger."""
        
        debug_format = "%(asctime)s (%(levelname)s) %(namespace)s : %(message)s"
        """The logging format for both file and console if ``debug==True``."""
        
        clear_loggers = True
        """Whether of not to clear previous loggers first."""
        
        # These are the default config values, overridden by any '[log]' 
        # section in parsed config files.
        config_section = 'log'
        """
        The section of the application configuration that holds this handlers
        configuration.
        """
        
        config_defaults = dict(
            file=None,
            level='INFO',
            to_console=True,
            rotate=False,
            max_bytes=512000,
            max_files=4,
            )
        """
        The default configuration dictionary to populate the ``log`` section.
        """
            
    levels = ['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']

    def __init__(self, *args, **kw):
        super(LoggingLogHandler, self).__init__(*args, **kw)
        self.app = None
        
    def _setup(self, app_obj):
        super(LoggingLogHandler, self)._setup(app_obj)
        self._meta._merge(self.app.config.get_section_dict('log'))
        
        if self._meta.namespace is None:
            self._meta.namespace = self.app._meta.label

        self.backend = logging.getLogger(self._meta.namespace)
        
        # the king trumps all
        if is_true(self.app._meta.debug):
            self._meta.level = 'DEBUG'
            
        self.set_level(self._meta.level)
        
        # clear loggers?
        if is_true(self._meta.clear_loggers):
            self.clear_loggers()
            
        # console
        if is_true(self._meta.to_console):
            self._setup_console_log()
        
        # file
        if self._meta.file:
            self._setup_file_log()
            
        self.debug("logging initialized for '%s' using LoggingLogHandler" % \
                   self._meta.namespace)
                 
    def set_level(self, level):
        """
        Set the log level.  Must be one of the log levels configured in 
        self.levels which are ``['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']``.
        
        :param level: The log level to set.
        
        """
        if level not in self.levels:
            level = 'INFO'
        level = getattr(logging, level.upper())
        
        self.backend.setLevel(level)  
        
        for handler in logging.getLogger(self._meta.namespace).handlers:
            handler.setLevel(level)
            
    def clear_loggers(self):
        """Clear any previously configured logging namespaces."""
        
        if not self._meta.namespace:
            # _setup() probably wasn't run
            return
            
        for i in logging.getLogger(self._meta.namespace).handlers:
            logging.getLogger(self._meta.namespace).removeHandler(i)
            self.backend = logging.getLogger(self._meta.namespace)
    
    def _setup_console_log(self):
        """Add a console log handler."""
        
        console_handler = logging.StreamHandler()
        if self.level() == logging.getLevelName(logging.DEBUG):
            format = logging.Formatter(self._meta.debug_format)
        else:
            format = logging.Formatter(self._meta.console_format)
        console_handler.setFormatter(format)    
        console_handler.setLevel(getattr(logging, self.level()))   
        self.backend.addHandler(console_handler)
    
    def _setup_file_log(self):
        """Add a file log handler."""
        
        file = os.path.abspath(os.path.expanduser(self._meta.file))
        log_dir = os.path.dirname(file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        if self._meta.rotate:
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                file, 
                maxBytes=int(self._meta.max_bytes), 
                backupCount=int(self._meta.max_files),
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(file)
        
        if self.level() == logging.getLevelName(logging.DEBUG):
            format = logging.Formatter(self._meta.debug_format)
        else:
            format = logging.Formatter(self._meta.file_format)
        file_handler.setFormatter(format)   
        file_handler.setLevel(getattr(logging, self.level())) 
        self.backend.addHandler(file_handler)
        
    def level(self):
        """Returns the current log level."""
        
        return logging.getLevelName(self.backend.level)
    
    def _get_logging_kwargs(self, namespace, **kw):
        if namespace is None:
            namespace = self._meta.namespace
            
        if 'extra' in kw.keys() and 'namespace' in kw['extra'].keys():
            pass
        elif 'extra' in kw.keys() and 'namespace' not in kw['extra'].keys():
            kw['extra']['namespace'] = namespace
        else:
            kw['extra'] = dict(namespace=namespace)
        
        return kw
        
    def info(self, msg, namespace=None, **kw):
        """
        Log to the INFO facility.
        
        :param msg: The message the log.
        :param namespace: A log prefix, generally the module ``__name__`` that 
            the log is coming from.  Will default to self._meta.namespace if 
            None is passed.
        :keyword kw: Keyword arguments are passed on to the backend logging 
            system.
            
        """
        kwargs = self._get_logging_kwargs(namespace, **kw)
        self.backend.info(msg, kwargs)
        
    def warn(self, msg, namespace=None, **kw):
        """
        Log to the WARN facility.
        
        :param msg: The message the log.
        :param namespace: A log prefix, generally the module ``__name__`` that 
            the log is coming from.  Will default to self._meta.namespace if 
            None is passed.
        :keyword kw: Keyword arguments are passed on to the backend logging 
            system.
            
        """
        kwargs = self._get_logging_kwargs(namespace, **kw)
        self.backend.warn(msg, kwargs)
    
    def error(self, msg, namespace=None, **kw):
        """
        Log to the ERROR facility.
        
        :param msg: The message the log.
        :param namespace: A log prefix, generally the module ``__name__`` that 
            the log is coming from.  Will default to self._meta.namespace if 
            None is passed.
        :keyword kw: Keyword arguments are passed on to the backend logging 
            system.
            
        """
        kwargs = self._get_logging_kwargs(namespace, **kw)
        self.backend.error(msg, kwargs)
    
    def fatal(self, msg, namespace=None, **kw):
        """
        Log to the FATAL (aka CRITICAL) facility.
        
        :param msg: The message the log.
        :param namespace: A log prefix, generally the module ``__name__`` that 
            the log is coming from.  Will default to self._meta.namespace if 
            None is passed.
        :keyword kw: Keyword arguments are passed on to the backend logging 
            system.
            
        """
        kwargs = self._get_logging_kwargs(namespace, **kw)
        self.backend.fatal(msg, kwargs)
    
    def debug(self, msg, namespace=None, **kw):
        """
        Log to the DEBUG facility.
        
        :param msg: The message the log.
        :param namespace: A log prefix, generally the module ``__name__`` that 
            the log is coming from.  Will default to self._meta.namespace if 
            None is passed.  For debugging, it can be useful to set this to 
            ``__file__``, though ``__name__`` is much less verbose.
        :keyword kw: Keyword arguments are passed on to the backend logging 
            system.
                        
        """
        kwargs = self._get_logging_kwargs(namespace, **kw)
        self.backend.debug(msg, **kwargs)


def load():
    """Called by the framework when the extension is 'loaded'."""
    handler.register(LoggingLogHandler)
