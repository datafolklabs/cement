"""
The Argcomplete Extension provides the necessary hooks to utilize
the `Argcomplete Library <https://argcomplete.readthedocs.org/en/latest/>`_,
and perform auto-completion of command line arguments/options/sub-parsers/etc.

Requirements
------------

 * Argcomplete (``pip install argcomplete``)
 * Argparse


This extension currently only works when using
:class:`cement.ext.ext_argparse.ArgparseArgumentHandler` (default) and
:class:`cement.ext.ext_argparse.ArgparseController` (new in Cement 2.8).  It
will not work with :class:`cement.core.controller.CementBaseController`.


Configuration
-------------

This extension does not honor any application configuration settings.


Usage
-----

**myapp.py**

.. code-block:: python

    #!/usr/bin/env python

    from cement.core.foundation import CementApp
    from cement.ext.ext_argparse import ArgparseController, expose


    class BaseController(ArgparseController):
        class Meta:
            label = 'base'
            arguments = [
                (['-f', '--foo'], dict(help='base foo option', dest='foo'))
            ]

        @expose(hide=True)
        def default(self):
            print('Inside BaseController.default')

        @expose()
        def command1(self):
            print('Inside BaseController.command1')


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['argcomplete']
            handlers = [BaseController]

    with MyApp() as app:
        app.run()


Note the ``#!`` line, which allows us to call our script directly
(specifically for this example).  The Argcomplete library requires the
end-user to modify their environment in order to perform auto-completion.
For this example, we are using a non-global option for demonstration
purposes only.  In the *real world* you will need to setup Argcomplete for
your actual application entry-point name (i.e. ``myapp`` if installed as
``/usr/bin/myapp``, etc).

.. code-block:: console

    $ eval "$(register-python-argcomplete myapp.py)"

    $ ./myapp.py [tab][tab]

    --debug                              -h
    -o                                   --help
    --quiet                              command1
                                         default

See the
`Argcomplete Documentation <https://argcomplete.readthedocs.org/en/latest/>`_
on how to properly integrate it's usage into your application deployment.
This extension simply enables Argcomplete to do it's thing on application
startup.

"""

import argcomplete


def argparse_autocompletion(app):
    # Argcomplete doesn't support hidden options currently, so lets atleast
    # exclude our special options in ArgparseController
    exclude = []
    if hasattr(app, 'controller') and app.controller is not None:
        if hasattr(app.controller, '_dispatch_option'):
            exclude.append(app.controller._dispatch_option)
        if hasattr(app.controller, '_controller_option'):
            exclude.append(app.controller._controller_option)

    argcomplete.autocomplete(app.args, exclude=exclude)


def load(app):
    app.hook.register('pre_argument_parsing',
                      argparse_autocompletion, weight=99)
