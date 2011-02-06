Logging
=======

Cement applications are setup with the standard logging facility for both
file and console logging.  

Configuration Settings
----------------------

The following configuration options under your applicaitons [root] namespace
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
    

Configuring Logging via a Config File
-------------------------------------

FIX ME