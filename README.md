Cement CLI Application Framework for Python
===========================================

Cement is an advanced CLI Application Framework for Python.  Its goal is to
introduce a standard, and feature-full platform for both simple and complex
command line applications as well as support rapid development needs without
sacrificing quality.

[![Continuous Integration Status](https://travis-ci.org/datafolklabs/cement.png)](https://travis-ci.org/datafolklabs/cement)

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
 * Zero external dependencies* (not including optional extensions)
 * 100% test coverage using Nose*
 * 100% PEP8 compliant using `pep8` and `autopep8` tools
 * Extensive Sphinx documentation
 * Tested on Python 2.6, 2.7, 3.2, and 3.3

*Note that argparse is required as an external dependency for Python < 2.7
and < 3.2.  Additionally, some *optional* extensions that are shipped with the
mainline Cement sources do require external dependencies.  It is the
responsibility of the application developer to include these dependencies
along with their application, as Cement explicitly does not include them.*


More Information
----------------

 * DOCS: http://builtoncement.com/2.2/
 * CODE: http://github.com/datafolklabs/cement/
 * PYPI: http://pypi.python.org/pypi/cement/
 * SITE: http://builtoncement.com/
 * T-CI: https://travis-ci.org/datafolklabs/cement
 * HELP: cement@librelist.org - #cement

License
-------

The Cement CLI Application Framework is Open Source and is distributed under
the BSD License (three clause).  Please see the LICENSE file included with
this software.
