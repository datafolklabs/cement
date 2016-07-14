.. Cement documentation master file, created by
   sphinx-quickstart on Mon Aug 22 17:52:04 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cement Framework
================

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

.. image:: https://secure.travis-ci.org/datafolklabs/cement.svg
  :target: https://travis-ci.org/#!/datafolklabs/cement
.. image:: https://badges.gitter.im/Join%20Chat.svg
  :target: https://gitter.im/datafolklabs/cement

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
 * 100% test coverage using ``nose`` and ``coverage``
 * 100% PEP8 and style compliant using ``flake8``
 * Extensive Sphinx documentation
 * Tested on Python 2.6, 2.7, 3.3, 3.4, 3.5

*Note that argparse is required as an external dependency for Python < 2.7
and < 3.2.  Additionally, some optional extensions that are shipped with
the mainline Cement sources do require external dependencies.  It is the
responsibility of the application developer to include these dependencies
along with their application if they intend to use any optional extensions
that have external dependencies, as Cement explicitly does not include them.*


Getting More Information
------------------------

 * DOCS: http://builtoncement.com/2.10/
 * CODE: http://github.com/datafolklabs/cement/
 * PYPI: http://pypi.python.org/pypi/cement/
 * SITE: http://builtoncement.com/
 * T-CI: http://travis-ci.org/datafolklabs/cement
 * HELP: cement@librelist.org - #cement - gitter.im/datafolklabs/cement


Mailing List
------------

Sign up for the Cement Framework mailing list to recieve updates regarding
new releases, important features, and other related news.  This not an open
email thread, but rather an extremely minimal, low noise announcement only 
list.  You can unsubscribe at any time.

.. raw:: html

    <!-- Begin MailChimp Signup Form -->
    <link href="http://cdn-images.mailchimp.com/embedcode/slim-081711.css" rel="stylesheet" type="text/css">
    <style type="text/css">
      #mc_embed_signup{background:#fff; clear:left; font:14px Helvetica,Arial,sans-serif; }
      /* Add your own MailChimp form style overrides in your site stylesheet or in this style block.
         We recommend moving this block and the preceding CSS link to the HEAD of your HTML file. */
    </style>
    <div id="mc_embed_signup">
    <form action="http://datafolklabs.us7.list-manage.com/subscribe/post?u=444ce23fdf1c30e830f893b57&amp;id=7be3a6a31e" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
        <div id="mc_embed_signup_scroll">
      
      <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" placeholder="email address" required>
        <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
        <div style="position: absolute; left: -5000px;"><input type="text" name="b_444ce23fdf1c30e830f893b57_7be3a6a31e" tabindex="-1" value=""></div>
        <div class="clear"><input type="submit" value="Subscribe" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
        </div>
    </form>
    </div>
    <BR />

    <!--End mc_embed_signup-->


Documentation
-------------

.. toctree::
   :maxdepth: 1

   changes
   license
   contributors
   upgrading
   whats_new
   projects_built_on_cement
   faq
   api/index

.. toctree::
   :maxdepth: 2

   dev/index

.. toctree::
   :maxdepth: 2

   examples/index


