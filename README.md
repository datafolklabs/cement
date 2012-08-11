Cement CLI Application Framework for Python
===========================================

Cement is an advanced CLI Application Framework for Python.  Its goal is to 
introduce a standard, and feature-full platform for both simple and complex 
command line applications as well as support rapid development needs without 
sacrificing quality.

[![Continuous Integration Status](https://secure.travis-ci.org/cement/cement.png)](http://travis-ci.org/cement/cement)

Cement core features include (but are not limited to):

 * Core pieces of the framework are customizable via handlers/interfaces
 * Extension handler interface to easily extend framework functionality
 * Config handler supports parsing multiple config files into one config
 * Argument handler parses command line arguments and merges with config
 * Log handler supports console and file logging
 * Plugin handler provides an interface to easily extend your application
 * Hook support adds a bit of magic to apps and also ties into framework
 * Handler system connects implementation classes with Interfaces
 * Output handler interface renders return dictionaries to console
 * Cache handler interface adds caching support for improved performance
 * Controller handler supports sub-commands, and nested controllers
 * Zero external dependencies* (ext's with dependencies ship separately)
 * 100% test coverage
 * Extensive Sphinx documentation
 * Tested on Python 2.6, 2.7, 3.1, and 3.2

*Note that argparse is required as an external dependency for Python < 2.7 
and < 3.2.*


More Information
----------------

 * DOCS: http://builtoncement.com/2.0/
 * CODE: http://github.com/cement/
 * PYPI: http://pypi.python.org/pypi/cement/
 * SITE: http://builtoncement.com/
 * T-CI: http://travis-ci.org/cement/cement
 * HELP: cement@librelist.org - #cement
    
License
-------

The Cement CLI Application Framework is Open Source and is distributed under 
the BSD License (three clause).  Please see the LICENSE file included with 
this software.  
