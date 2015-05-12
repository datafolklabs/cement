.. _whats_new:

What's New
==========

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
