.. _whats_new:

What's New
==========

New Features in Cement 2.10
---------------------------

Support for Multiple File Plugin Directories
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prior to Cement 2.10, application plugins were only supported as single files
such as ``myplugin.py``.  Plugins can now be a single file, or full python 
modules like ``myplugin/__init__.py``.

An example plugin might look like:

.. code-block:: console

    myplugin/
        __init__.py
        controllers.py
        templates/
            cmd1.mustache
            cmd2.mustache
            cmd3.mustache

The only thing required in a plugin is that it supply a ``load()`` function
either in a ``myplugin.py`` or ``myplugin/__init__.py``.  The rest is up to 
the developer.

See :ref:`Application Plugins <application_plugins>` for more information.

Related:

    * :issue:`350`


Cross Platform Filesystem Event Monitoring via Watchdog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Applications can now monitor, and react to, filesystem events with a very
easy wrapper around the
`Watchdog <https://pypi.python.org/pypi/watchdog>`_ library.  The extension
makes it possible to add a list of directories to monitor, and link them
with the class to handle any events while automating the proper setup, and
teardown of the backend observer.

The Watchdog Extension will make it possible in future releases to
properly handle reloading a running application any time configuration files
are modified (partially implemented by the `reload_config` extension that has
limitations and does not support reloading the app).  Another common use case
is the ability to reload a long running process any time source files are
modified which will be useful for development when working on daemon-like apps 
so that the developer doesn't need to stop/start everytime changes are made.

See the :ref:`Watchdog Extension <cement.ext.ext_watchdog>` for more
information.

Related:

    * :issue:`326`
    * :issue:`394`


Ability To Pass Meta Defaults From CementApp.Meta Down To Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cement handlers are often referenced by their label, and not passed as
pre-instantiated objects which requires the framework to instantiate them
dynamically with no keyword arguments.

For example:

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['json']

In the above, Cement will load the ``json`` extension, which
registers ``JsonOutputHandler``.  When it comes time to recall that handler,
it is looked up as ``output.json`` where ``output`` is the handler type
(interface) and ``json`` is the handler label.  The class is then instantiated
without any arguments or keyword arguments before use.  If a developer needed
to override any meta options in ``JsonOutputHandler.Meta`` they would
**previously** have had to sub-class it.  Consider the following example,
where we sub-class ``JsonOutputHandler`` in order to override
``JsonOutputHandler.Meta.json_module``:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.ext.ext_json import JsonOutputHandler

    class MyJsonOutputHandler(JsonOutputHandler):
        class Meta:
            json_module = 'ujson'
    
    def override_json_output_handler(app):
        app.handler.register(MyJsonOutputHandler, force=True)

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['json']
            hooks = [
                ('post_setup', override_json_output_handler)
            ]


If there were anything else in the ``JsonOutputHandler`` that the developer
needed to subclass, this would be fine.  However the purpose of the above is
soley to override ``JsonOutputHandler.Meta.json_module``, which is tedious.

As of Cement 2.10, the above can be accomplished more-easily by the following
by way of ``CementApp.Meta.meta_defaults`` (similar to how ``config_defaults``
are handled:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.utils.misc import init_defaults

    META = init_defaults('output.json')
    META['output.json']['json_module'] = 'ujson'

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['json']
            output_handler = 'json'
            meta_defaults = META


When ``JsonOutputHandler`` is instantiated, the defaults from
``META['output.json']`` will be passed as ``**kwargs`` (overriding builtin
meta options).

Related:

    * :issue:`395`


Additional Extensions
^^^^^^^^^^^^^^^^^^^^^

    * :ref:`Jinja2 <cement.ext.ext_jinja2>` - Provides template based output
      handling using the Jinja2 templating language
    * :ref:`Redis <cement.ext.ext_redis>` - Provides caching support using 
      Redis backend
    * :ref:`Watchdog <cement.ext.ext_watchdog>` - Provides cross-platform
      filesystem event monitoring using the Watchdog library.
    * :ref:`Handlebars <cement.ext.ext_handlebars>` - Provides template based 
      output handling using the Handlebars templating language



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


When the ``with`` statement is initialized, the ``app`` object is created, and 
then right away ``app.setup()`` is called before entering the block.  When
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
