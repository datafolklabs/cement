"""Logging Framework Extension"""

import os
import logging
from ..core import exc, log, handler
from ..utils.misc import is_true
from ..utils import fs

class LoggingLogHandler(log.CementLogHandler):  
    """
    This class is an implementation of the :ref:`ILog <cement.core.log>` 
    interface, and sets up the logging facility using the standard Python
    `logging <http://docs.python.org/library/logging.html>`_ module. 
    
    Configuration Options
    
    The following configuration options are recognized in this class:
    
        log.level
        
        log.file
        
        log.to_console
        
        log.rotate
        
        log.max_bytes
        
        log.max_files
    
    
    A sample config section (in any config file) might look like:
    
    .. code-block:: text

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
        if self._meta.namespace is None:
            self._meta.namespace = self.app._meta.label
            
        self.backend = logging.getLogger(self._meta.namespace)
        
        # hack for application debugging
        if is_true(self.app._meta.debug):
            self.app.config.set('log', 'level', 'DEBUG')
            
        self.set_level(self.app.config.get('log', 'level'))
        
        # clear loggers?
        if is_true(self._meta.clear_loggers):
            self.clear_loggers()
            
        # console
        if is_true(self.app.config.get('log', 'to_console')):
            self._setup_console_log()
        
        # file
        if self.app.config.get('log', 'file'):
            self._setup_file_log()
        
        
        self.debug("logging initialized for '%s' using LoggingLogHandler" % \
                   self._meta.namespace)

    def set_level(self, level):
        """
        Set the log level.  Must be one of the log levels configured in 
        self.levels which are ``['INFO', 'WARN', 'ERROR', 'DEBUG', 'FATAL']``.
        
        :param level: The log level to set.
        
        """
        level = level.upper()
        if level not in self.levels:
            level = 'INFO'
        level = getattr(logging, level.upper())
        
        self.backend.setLevel(level)  
        
        for handler in logging.getLogger(self._meta.namespace).handlers:
            handler.setLevel(level)

    def get_level(self):
        """Returns the current log level."""
        return logging.getLevelName(self.backend.level)
           
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
        if self.get_level() == logging.getLevelName(logging.DEBUG):
            format = logging.Formatter(self._meta.debug_format)
        else:
            format = logging.Formatter(self._meta.console_format)
            
        console_handler.setFormatter(format)    
        console_handler.setLevel(getattr(logging, self.get_level()))   
        self._console_handler = console_handler
        self.backend.addHandler(console_handler)
    
    def _setup_file_log(self):
        """Add a file log handler."""
        file_path = fs.abspath(self.app.config.get('log', 'file'))
        log_dir = os.path.dirname(file_path)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        if self.app.config.get('log', 'rotate'):
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                file_path, 
                maxBytes=int(self.app.config.get('log', 'max_bytes')), 
                backupCount=int(self.app.config.get('log', 'max_files')),
                )
        else:
            from logging import FileHandler
            file_handler = FileHandler(file_path)
        
        if self.get_level() == logging.getLevelName(logging.DEBUG):
            format = logging.Formatter(self._meta.debug_format)
        else:
            format = logging.Formatter(self._meta.file_format)
        file_handler.setFormatter(format)   
        file_handler.setLevel(getattr(logging, self.get_level())) 
        
        self._file_handler = file_handler
        self.backend.addHandler(file_handler)
    
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
        self.backend.info(msg, **kwargs)
        
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
        self.backend.warn(msg, **kwargs)
    
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
        self.backend.error(msg, **kwargs)
    
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
        self.backend.fatal(msg, **kwargs)
    
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
