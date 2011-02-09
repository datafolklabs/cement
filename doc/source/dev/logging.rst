Logging
=======

Cement applications are setup with the standard logging facility for both
file and console logging.  

Configuration Settings
----------------------

The following configuration options under your applications [root] namespace
are honored:

    log_file
        A path to a log file (if none is set, file logging is disabled)
        
    log_level
        Log level (info, warn, error, fatal, debug)
        
    log_to_console
        Whether or not to log to console.
        
    logging_config_file
        A logging configuration file that allows you to override the default
        logging configuration.  File format and usage can be found here:
        http://docs.python.org/library/logging.html#logging.fileConfig
        
    log_max_bytes
        Maximum number of bytes to keep in a log file (default: no limit).

    log_max_files
        Maximum number of log files to keep in rotation (default: no rotation)
    

Using the Logger
----------------

.. code-block:: python
    
    from cement.core.log import get_logger
    
    log = get_logger(__name__)
    log.info('this is an info message')
    log.warn('this is a warning')
    log.error('this is an error')
    log.fatal('this is a critical error')
    log.debug('KAPLA!!!!!!')
    
    
Configuring Logging via a Config File
-------------------------------------

An example logging configuration file might look like:

*/etc/yourapp/yourapp-logging.conf*
    
.. code-block:: text

    [loggers]
    keys = root

    [handlers]
    keys = hand01

    [formatters]
    keys = form01

    [logger_root]
    level=DEBUG
    handlers=hand01

    [handler_hand01]
    class=StreamHandler
    level=NOTSET
    formatter=form01
    args=(sys.stdout,)

    [formatter_form01]
    format=F1 %(asctime)s %(levelname)s %(message)s
    datefmt=
    class=logging.Formatter
    