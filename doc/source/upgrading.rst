.. _upgrading:

Upgrading
=========

This section outlines any information and changes that might need to be made
in order to update your application built on previous versions of Cement.

Upgrading from 2.8.x to 2.9.x
-----------------------------

Cement 2.9 introduces a few incompatible changes from the previous 2.8 stable
release, as noted in the :ref:`ChangeLog <changelog>`.

Deprecated: cement.core.interface.list()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This function should no longer be used in favor of 
``CementApp.handler.list_types()``.  It will continue to work throughout 
Cement 2.x, however is not compatible if 
``CementApp.Meta.use_backend_globals == False``.

Related: 

 * :issue:`366`
 * :issue:`376`


Upgrading from 2.6.x to 2.8.x
-----------------------------

Cement 2.8 introduced a few incompatible changes from the previous 2.6 stable
release, as noted in the :ref:`ChangeLog <changelog>`.

TypeError: my_signal_hook() takes exactly 2 arguments (3 given)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Cement 2.6, functions registered to the ``signal`` hook were only 
expected/required to accept the ``signum`` and ``frame`` arguments, however
``signal`` hook functions must now also accept the ``app`` object as an 
argument as well.

After upgrading to Cement 2.8, you might receive something similar to the 
following exception:

.. code-block:: console

    TypeError: my_signal_hook() takes exactly 2 arguments (3 given)


The fix is to simply prefix any ``signal`` hook functions with an ``app`` 
argument.

For example:

.. code-block:: python

    def my_signal_hook(signum, frame):
        pass

Would need to be:

.. code-block:: python

    def my_signal_hook(app, signum, frame):
        pass


Related:

    * :issue:`311`


TypeError: render() got an unexpected keyword argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Cement 2.6, output handlers were not required to accept ``**kwargs``, 
however this is now required to allow applications to mix different types of 
output handlers together that might support different features/usage.  

After upgrading to Cement 2.8, you might receive something similar to the 
following exception:

.. code-block:: console

    TypeError: render() got an unexpected keyword argument


This would most likely be the case because you have created your own custom
output handler, or are using a third-party output handler that has not been
updated to support Cement 2.8 yet.  The fix is to simply add ``**kwargs`` to 
the end of the `render()` method.

For example:

.. code-block:: python

    def render(self, data):
        pass

Would need to be:

.. code-block:: python

    def render(self, data, **kwargs):
        pass


CementApp.Meta.exit_on_close Defaults to False
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Cement 2.6, the feature to call ``sys.exit()`` when ``app.close()`` is 
called was implemented, however defaulting it to ``True`` is not the ideal 
behavior.  The default is now ``False``, making it the developers option to 
explicitly enable it.

To revert the change, and default ``exit_on_close`` to ``True``, simply set it
in ``CementApp.Meta.exit_on_close``:

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            exit_on_close = True


Upgrading from 2.4.x to 2.6.x
-----------------------------

Cement 2.6 introduced a few incompatible changes from the previous 2.4 stable
release, as noted in the :ref:`ChangeLog <changelog>`.

InterfaceError: Invalid handler ... missing '_meta.label'.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prior to Cement 2.5.2, ``CementBaseController.Meta.label`` defaulted to 
``base``.  The new default is ``None``, causing the potential for breakage of
a controller that did not explicity set the ``label`` meta option.

You can resolve this error by explicity setting the ``label`` meta option:

.. code-block:: python

    class MyBaseController(CementBaseController):
        class Meta:
            label = 'base'


Upgrading from 2.2.x to 2.4.x
-----------------------------

Cement 2.4 introduced a few incompatible changes from the previous 2.2 stable
release, as noted in the :ref:`ChangeLog <changelog>`.

Related:

    * :issue:`308`


CementApp.render() Prints Output Without Calling print()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before Cement 2.3.2 the ``app.render()`` function did not actually print
anything, therefore you would have to call ``print app.render()``.  This
now defaults to writing output to ``sys.stdout``, but can be modified for the
older behavior by passing ``out=None`` when calling it:

.. code-block:: python

    app.render(data, out=None)


Additionally, you can also now write directly to a file:

.. code-block:: python

    myfile = open('/path/to/myfile', 'w')
    app.render(data, out=myfile)
    myfile.close()


error: unrecognized arguments: --json/--yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After upgrading to Cement > 2.3.2 you might encounter the error:

.. code-block:: text

    error: unrecognized arguments: --json


Or similar errors like:

.. code-block:: text

    error: unrecognized arguments: --yaml


This is due to a design change, and a new feature allowing the end user to
optionally override handlers via command line.  Rather than having a unique
option for every type of output handler, you now have one option that allows
overriding the defined output handler by passing it the handler label.

Note that only handlers that have ``overridable = True`` in their meta-data
will be valid options.

To resolve this issue, you simply need to pass ``-o json`` or ``-o yaml`` at
command line to override the default output handler.

Related:

    * :issue:`229`


NoSectionError: No section: 'log'
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After upgrading to Cement > 2.3.2 you might encounter the error:

.. code-block:: text

    NoSectionError: No section: 'log'


In previous versions of Cement < 2.3.2, the default logging configuration
section in the config file was ``[log]``.  This has been changed to
``[log.logging]`` in order to be consistent with all other handler
configuration sections.

Another issue you might encounter due to the above change is that log related
configuration settings read from a configuration file would no longer work.
The necessary change to resolve this issue is to change all references of
``log`` in relation to the log configuration section, to ``log.logging``.


Related:

    * :issue:`227`


TypeError: load() takes no arguments (1 given)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After upgrading to Cement > 2.3.2 you might encounter the error:

.. code-block:: text

    TypeError: load() takes no arguments (1 given)


Previous versions of Cement < 2.3.2 did not require an `app` argument to be
passed to the `load()` functions of extensions/plugins/bootstrap modules.
In Cement > 2.3.2 all extension/plugins/bootstrap modules must accept a single
argument named `app` which is the application object in its current state when
`load()` is called.

To resolve this issue simply modify all relevant `load()` functions to accept
the `app` argument.  For example:

.. code-block:: python

    def load():
        pass

To:

.. code-block:: python

    def load(app):
        pass


Upgrading from 2.0.x to 2.2.x
-----------------------------

Cement 2.2 introduced a few incompatible changes from the previous 2.0 stable
release, as noted in the :ref:`Changelog <changelog>`.

ImportError: cannot import name version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When attempting to install Cement > 2.1 on a system that already has an older
version of Cement < 2.1 you will likely run into this error:

.. code-block:: text

    ImportError: cannot import name version


Currently we do not have a way to resolve this programatically in Cement.  The
resolution is to remove the older version of Cement < 2.1, and then re-install
the newer version.

Related:

    * :issue:`237`


FrameworkError: Duplicate Arguments/Commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After upgrading, you might encounter one or both of the following errors
related to application controllers:

.. code-block:: text

    cement.core.exc.FrameworkError: Duplicate command named 'mycommand' found
    in controller '<__main__.MySecondController object at 0x10669ab50>'


.. code-block:: text

    cement.core.exc.FrameworkError: argument -f/--foo: conflicting option
    string(s): -f, --foo


This is likely due to a change in how application controllers are configured.
By default, all controllers are of type `embedded`, meaning that their
arguments and commands are added to the parent controller.  To resolve this
issue you can change the `stacked_type` to `nested`, meaning that the stacked
controller will be an additional sub-command under the parent (nesting a new
level commands/arguments).

For example:

.. code-block:: python

    class MyStackedController(CementBaseController):
        class Meta:
            label = 'my_stacked_controller'
            stacked_on = 'base'
            stacked_type = 'nested'

Related:

    * :issue:`234`

Discontinued use of Setuptools Namespace Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Previous versions of Cement utilitized Setuptools namespace packages in order
to allow external libraries (such as optional framework extensions) to use the
``cement.ext`` namespace.  Meaning that an extension packaged separately could
use the namespace ``cement.ext.ext_myextension`` and be imported from the
``cement.ext`` namespace as if it were shipped with the mainline sources
directly.  This indirectly caused issues with certain IDE's due to the fact
that namespace packages do not install a proper ``__init__.py`` and are
handled differently by Setuptools.

With the move to merging optional extenions into mainline sources, we no
longer require the use of Setuptools namespace packages.  That said, if a
developer had created their own extension using the ``cement.ext`` namespace,
that extension would no longer work or worse may confusing Python into
attempting to load ``cement.ext`` from the extension and not Cement causing
even bigger problems.

To resolve this issue, simply change the extension module to anything
other than ``cement.ext``, such as ``myapp.ext``.

Related:

    * :issue:`202`


LoggingLogHandler Changes
^^^^^^^^^^^^^^^^^^^^^^^^^

The ``clear_loggers`` meta option is now a ``list``, rather than a
``boolean``.  Therefore, rather than telling LoggingLogHandler to 'clear
all previously defined loggers', you are telling it to 'clear only these
previously defined loggers' in the list.

If your application utilizied the ``LoggingLogHandler.Meta.clear_loggers``
option, you would simply need to change it from a ``boolean`` to a list of
loggers such as ``['myapp', 'some_other_logging_namespace']``.


Related:

    * :issue:`163`


ConfigParserConfigHandler Changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``ConfigParserConfigHandler.has_key()`` function has been removed.  To
update your application for these changes, you would look for all code
similar to the following:

.. code-block:: python

    if myapp.config.has_key('mysection', 'mykey'):
        # ...


And modify it to something similar to:

.. code-block:: python

    if 'mykey' in myapp.config.keys('mysection'):
        # ...


Related:

    * :issue:`173`


CementApp Changes
^^^^^^^^^^^^^^^^^

The ``CementApp.get_last_rendered()`` function has been deprected.  Developers
should now use the ``CementApp.last_rendered`` property instead.  To update
your application for these changes, you would look for all code similar to:

.. code-block:: python

    CementApp.get_last_rendered()


And modify it to something similar to:

.. code-block:: python

    CementApp.last_rendered


Related:

    * :issue:`201` - Add Deprecation Warning for CementApp.get_last_rendered()


CementBaseController Changes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All short-cuts such as ``log``, ``pargs``, etc have been removed from
CementBaseController due to the fact that these class members could clash
if the developer added a command/function of the same name.  To update
your application for these changes, in any classes that subclass from
``CementBaseController``, you might need to modify references to ``self.log``,
``self.pargs``, etc to ``self.app.log``, ``self.app.pargs``, etc.

Additionally, if you wish to re-implement these or other shortcuts, you can
do so by overriding ``_setup()`` in your controller code, and add something
similar to the following:

.. code-block:: python

    def _setup(self, *args, **kw):
        res = super(MyClass, self)._setup(*args, **kw)
        self.log = self.app.log
        self.pargs = self.app.pargs
        # etc

        return res


An additional change to ``CementBaseController`` is that the application's
``base`` controller attached to ``YourApp.Meta.base_controller`` now must
have a label of ``base``.  Previously, the base controller could have any
label however this is now a hard requirement.  To update your application
for these changes, simply change the label of your base controller to
``base``.

Finally, the ``CementBaseController`` used to have members called ``hidden``,
``visible``, and ``exposed`` which were each a list of controller functions
used for handling dispatch of commands, and how they are displayed in
``--help``.  These members no longer exist.

These members were never documented, and is very unlikely that anybody has
ever used them directly.  Updating your application for these changes would
be outside the scope of this document.

Related:

    * :issue:`141`
    * :issue:`167`
    * :issue:`179`


Backend Changes
^^^^^^^^^^^^^^^

Several backend pieces have been moved or renamed.  For example
``cement.core.backend.handlers`` is now ``cement.core.backend.__handlers__``,
etc.  The same goes for ``cement.core.backend.SAVED_STDOUT`` which is now
``cement.core.backend.__saved_stdout__``.  These are undocumented, and used
specifically by Cement.  It is unlikely that anyone has used these members
directly, and updating your application for these changes is outside the
scope of this document.  See ``cement.core.backend`` to assess what, if any,
change you may need to change in your code to compensate for these changes.

The ``cement.core.backend.defaults()`` function has moved to
``cement.utils.misc.init_defaults()``.  It's usage is exactly the same.

The ``cement.core.backend.minimal_logger()`` function has moved to
``cement.utils.misc.minimal_logger``.  It's usage is also the same.

Related:

    * :issue:`177`
    * :issue:`178`
