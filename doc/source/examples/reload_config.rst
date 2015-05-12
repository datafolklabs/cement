Auto Reload When Configuration Files Change
===========================================

Cement 2.5.2 added the **experimental** 
:ref:`Reload Config Extension <cement.ext.ext_reload_config>`, 
allowing applications built on Cement to automatically reload ``app.config``
any time configuration files and/or plugin configuration files are modified. 
Note that the ``ext_reload_config`` extension requires ``pyinotify`` and is
only supported on Linux.

Additionally, the extension adds the ``pre_reload_config`` and 
``post_reload_config`` hooks allowing applications to respond to the event and
perform actions when config changes are detected.

The following demonstrates how this can be accomplished:

.. code-block:: python

    from time import sleep
    from cement.core.exc import CaughtSignal
    from cement.core import hook
    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    def print_foo(app):
        print("Foo => %s" % app.config.get('myapp', 'foo'))


    class Base(CementBaseController):
        class Meta:
            label = 'base'

        @expose(hide=True)
        def default(self):
            print('Inside Base.default()')

            # simulate a long running process
            while True:
                sleep(30)

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            extensions = ['reload_config']
            hooks = [('post_reload_config', print_foo)]
            handlers = [Base]


    with MyApp() as app:
        try:
            app.run()
        except CaughtSignal as e:
            # maybe do something... but catch it regardless so app.close() is
            # called when exiting `with` cleanly.
            print(e)


The output looks something like:

.. code-block:: console

    $ python myapp.py --debug

    Inside Base.default()
    
    2015-05-12 19:05:34,372 (DEBUG) cement.ext.ext_reload_config : config path modified: mask=IN_CLOSE_WRITE, path=/home/vagrant/.myapp.conf
    2015-05-12 19:05:34,373 (DEBUG) cement.core.config : config file '/home/vagrant/.myapp.conf' exists, loading settings...
    2015-05-12 19:05:34,373 (DEBUG) cement.core.hook : running hook 'post_reload_config' (<function print_foo at 0x7f6b4d401b70>) from __main__
    Foo => bar1

    2015-05-12 19:05:44,121 (DEBUG) cement.ext.ext_reload_config : config path modified: mask=IN_CLOSE_WRITE, path=/home/vagrant/.myapp.conf
    2015-05-12 19:05:44,122 (DEBUG) cement.core.config : config file '/home/vagrant/.myapp.conf' exists, loading settings...
    2015-05-12 19:05:44,122 (DEBUG) cement.core.hook : running hook 'post_reload_config' (<function print_foo at 0x7f6b4d401b70>) from __main__
    Foo => bar2
