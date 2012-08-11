.. Cement documentation master file, created by
   sphinx-quickstart on Mon Aug 22 17:52:04 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cement CLI Application Framework for Python
===========================================

Cement is an advanced CLI Application Framework for Python.  Its goal is to 
introduce a standard, and feature-full platform for both simple and complex 
command line applications as well as support rapid development needs without 
sacrificing quality.

.. image:: https://secure.travis-ci.org/cement/cement.png
  :target: http://travis-ci.org/#!/cement/cement

Core features include (but are not limited to):

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
 * Extensive documentation
 * Tested on Python 2.6, 2.7, 3.1, and 3.2

*Note that argparse is required as an external dependency for Python < 2.7 
and < 3.2.*


Getting More Information
------------------------

 * DOCS: http://builtoncement.com/2.0/
 * CODE: http://github.com/cement/
 * PYPI: http://pypi.python.org/pypi/cement/
 * SITE: http://builtoncement.com/
 * T-CI: http://travis-ci.org/cement/cement
 * HELP: cement@librelist.org - #cement

Documentation
-------------

.. toctree::
   :maxdepth: 1
   
   changes
   license
   contributors
   api/index    
   
.. toctree::
   :maxdepth: 2

   dev/index

.. toctree::
   :maxdepth: 2

   examples/index

  
