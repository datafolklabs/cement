.. Cement documentation master file, created by
   sphinx-quickstart on Mon Aug 22 17:52:04 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cement CLI Application Framework v2 Beta
========================================

Cement2 is an advanced CLI Application Framework for Python, and a complete
rewrite of Cement version 0.x/1.x.  Its goal is to introduce a standard, and 
feature-full platform for both simple and complex command line applications as 
well as support rapid development needs without sacrificing quality.

Cement2 Core features include (but are not limited to):

    * Core pieces of the framework are customizable via handlers/interfaces
    * Extension handler interface to easily extend framework functionality
    * Config handler supports parsing multiple config files into one config
    * Argument handler parses command line arguments and merges with config
    * Log handler supports console and file logging
    * Plugin handler provides an interface to easily extend your application
    * Hook support adds a bit of magic to apps and also ties into framework
    * Handler system connects implementation classes with Interfaces
    * Output handler interface renders return dictionaries to console
    * Core library and extensions have zero external dependencies
    * Extensions with external dependencies packaged separately
    * Controller handler supports sub-commands, and nested controllers
    * 98% Nose test coverage
    * Extensive Sphinx documentation
    * Tested on all major versions of Python 2.7 through 3.2
    

Cement2 Core Extensions includes:

    * JSON output handler extension (adds --json option)
    * YAML output handler extension (adds --yaml option)
    * ConfigObj config handler extension replaces ConfigParser
    * Damemon extension handles background processes (adds --daemon option)
    * Genshi output handler extension provides Text Templating


Other sites that might be helpful.

 * RTFD: http://cement.rtfd.org/en/portland/
 * CODE: https://github.com/derks/cement/tree/portland
 * PYPI: http://pypi.python.org/pypi/cement2
 *   CI: http://travis-ci.org/#!/derks/cement

Older Versions of Cement:

The current stable branch of Cement is 0.8. 

 * RTFD: http://cement.rtfd.org/en/latest/
 * CODE: http://github.com/derks/cement
 * PYPI: http://pypi.python.org/pypi/cement
 
Contents
--------

.. toctree::
   :maxdepth: 1
   
   changes
   license
   versions
   features
      
.. toctree::
   :maxdepth: 2

   api

.. toctree::
   :maxdepth: 2
       
   dev
