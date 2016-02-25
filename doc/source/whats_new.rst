.. _whats_new:

What's New
==========

New Features in Cement 2.8
--------------------------

ArgparseController
^^^^^^^^^^^^^^^^^^

Work has finally begun, and is mostly complete on the refactoring of
``CementBaseController``.  The new 
:class:`cement.ext.ext_argparse.ArgparseController` introduces the following
improvements:

    * Cleaner, and more direct use of ``Argparse``
    * Does not hijack ``Argparse`` usage in any way.
    * Provides an accessible ``sub-parser`` for every nested controller, 
      allowing the developer direct access to perform more advanced actions
      (argument grouping, mutually exclusive groups, etc).
    * Provides the ability to define arguments at both the controller level,
      as well as the sub-command level 
      (i.e. ``myapp controller sub-command {options}``).
    * Supports argument handling throughout the entire CLI chain
      (i.e. ``myapp {options} controller {options} sub-command {options}``)


The ``ArgparseController`` will become the default in Cement 3, however
``CementBaseController`` will remain the default in Cement 2.x.  Developers
are encouraged to begin porting to ``ArgparseController`` as soon possible,
as ``CementBaseController`` will be removed in Cement 3 completely.

Related:

    * :issue:`205`


Extensions
^^^^^^^^^^

    * :ref:`Argcomplete <cement.ext.ext_argcomplete>` - Provides the 
      ability to magically perform BASH autocompletion by simply loading the
      ``argcomplete`` extension.  (Requires ``ArgparseArgumentHandler`` and
      ``ArgparseController`` to function).
    * :ref:`Tabulate <cement.ext.ext_tabulate>` - Provides tabularized output
      familiar to users of MySQL, PGSQL, Etc.
    * :ref:`Alarm <cement.ext.ext_alarm>` - Provides quick access to 
      setting an application alarm to easily handling timing out long running
      operations.
    * :ref:`Memcached <cement.ext.ext_memcached>` - Now supported on Python 3. 


Misc Enhancements
^^^^^^^^^^^^^^^^^

    * Cement now supports the ability to reload runtime within the current
      process via ``app.reload()``.  This will enable future refactoring of
      the ``ext_reload_config`` extension that is intended to handle 
      reloading runtime after configuration files are modified.  This 
      affectively adds ``SIGHUP`` support.


New Features in Cement 2.6
--------------------------

Extensions
^^^^^^^^^^

    * :ref:`Reload Config <cement.ext.ext_reload_config>` - Provides the 
      ability to automatically reload ``app.config`` any time configuration
      files are modified.
    * :ref:`ColorLog <cement.ext.ext_reload_config>` - Provides colorized 
      logging to console (based on standard logging module).


Python With Statement Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the ``with`` statement makes setting up, running, and closing Cement apps
easier and cleaner.  The following is the recommended way of creating, and 
running Cement apps:

.. code-block:: python

    from cement.core.foundation import CementApp

    with CementApp('myapp') as app:
        app.run()


Or a more complete example:

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'

    with MyApp() as app:
        try:
            app.run()
        except Exception as e:
            # handle all your exceptions... this is just an example
            print('Caught Exception: %s' % e)


When the ``with`` statement is initialized, the ``app`` object is created, and then right away ``app.setup()`` is called before entering the block.  When
the ``with`` block is exited ``app.close()`` is also called.  This offers a
much cleaner approach, while still ensuring that the essential pieces are run
appropriately.  If you require more control over how/when ``app.setup()`` and
``app.close()`` are run, you can still do this the old way:

.. code-block:: python

    from cement.core.foundation import CementApp

    app = CementApp('myapp')
    app.setup()
    app.run()
    app.close()


But doesn't that just feel clunky?


**Related:**

    * :issue:`281`


Defining and Registering Hooks and Handlers from CementApp.Meta
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another improvement that lends itself nicely to code-cleanliness is the
ability to define and register hooks and handlers from within 
``CementApp.Meta``.  An example using application controllers and a simple
``pre_run`` hook looks like:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    def my_example_hook(app):
        pass

    class BaseController(CementBaseController):
        class Meta:
            label = 'base'


    class SecondController(CementBaseController):
        class Meta:
            label = 'second'


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            
            hooks = [
                ('pre_run', my_example_hook),
            ]

            handlers = [
                BaseController,
                SecondController,
            ]


**Related:**

    * :issue:`282`
