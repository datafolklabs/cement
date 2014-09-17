.. Cement documentation master file, created by
   sphinx-quickstart on Mon Aug 22 17:52:04 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cement Framework
================

.. warning:: This documentation is for the development version of Cement
    2.5.x.  For production please use, and reference the current stable
    version of `Cement 2.4.x <http://builtoncement.com/2.2/>`_ until this
    version is officially released as 2.6.x stable.

Cement is an advanced CLI Application Framework for Python.  Its goal is to
introduce a standard, and feature-full platform for both simple and complex
command line applications as well as support rapid development needs without
sacrificing quality.  Cement is flexible, and it's use cases span from the
simplicity of a micro-framework to the complexity of a mega-framework.
Whether it's a single file script, or a multi-tier application, Cement is the
foundation you've been looking for.

The first commit to Git was on Dec 4, 2009.  Since then, the framework has
seen several iterations in design, and has continued to grow and improve
since it's inception.  Cement is the most stable, and complete framework for
command line and backend application development.

.. image:: https://secure.travis-ci.org/datafolklabs/cement.png
  :target: https://travis-ci.org/#!/datafolklabs/cement

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
 * Zero external dependencies* of the core library
 * 100% test coverage using Nose
 * 100% PEP8 compliant using `pep8` and `autopep8` tools
 * Extensive Sphinx documentation
 * Tested on Python 2.6, 2.7, 3.2, and 3.3

*Note that argparse is required as an external dependency for Python < 2.7
and < 3.2.  Additionally, some optional extensions that are shipped with
the mainline Cement sources do require external dependencies.  It is the
responsibility of the application developer to include these dependencies
along with their application if they intend to use any optional extensions
that have external dependencies, as Cement explicitly does not include them.*


Getting More Information
------------------------

 * DOCS: http://builtoncement.com/2.5/
 * CODE: http://github.com/datafolklabs/cement/
 * PYPI: http://pypi.python.org/pypi/cement/
 * SITE: http://builtoncement.com/
 * T-CI: http://travis-ci.org/datafolklabs/cement
 * HELP: cement@librelist.org - #cement


Documentation
-------------

.. toctree::
   :maxdepth: 1

   changes
   license
   contributors
   upgrading
   faq
   api/index

.. toctree::
   :maxdepth: 2

   dev/index

.. toctree::
   :maxdepth: 2

   examples/index


