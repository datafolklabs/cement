.. _upgrading:

Upgrading
=========

This section outlines any information and changes that might need to be made
in order to update your application built on previous versions of Cement.

Upgrading from 2.0.x to 2.2.x
-----------------------------

Cement 2.2 introduced a few incompatible changes from the previous 2.0 stable
release, as noted in the :ref:`Changelog <changelog>`.

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
