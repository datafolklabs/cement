Append Config File Path via Command Line Option
===============================================

By default, Cement looks for config files in the following locations:

    * ``/etc/myapp/myapp.conf``
    * ``~/.myapp.conf``
    * ``~/.myapp/config``


You can modify this list by overriding ``CementApp.Meta.config_files`` in 
your application code, however a common use case for command line apps is the ability to override (or append to) the config file path(s) for the 
application via a command line option such as ``-C`` or ``--config``.  The 
following is a working example that demonstrates how you might accomplish that
by using a ``post_argument_parsing`` hook.  


**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    def append_config_path(app):
        if app.pargs.config_path:
            app._meta.config_files.append(app.pargs.config_path)
            app.config.parse_file(app.pargs.config_path)

    class Base(CementBaseController):
        class Meta:
            label = 'base'

            arguments = [
                (['-C'],
                 dict(help='append path to config files', 
                      dest='config_path', 
                      action='store', 
                      metavar='CONFIG')),
                ]

        @expose(hide=True)
        def default(self):
            print("Config Paths => %s" % self.app._meta.config_files)
            print("Foo => %s" % self.app.config.get('myapp', 'foo'))
        

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'

            handlers = [Base]

            hooks = [
                ('post_argument_parsing', append_config_path),
            ]

    with MyApp() as app:
        app.run()

**/etc/myapp/myapp.conf**

.. code-block:: console

    [myapp]
    foo = bar

**/path/to/another/myapp.conf**

.. code-block:: console

    [myapp]
    foo = bar2


This will look like:

.. code-block:: console

    $ python myapp.py
    Config Paths => ['/etc/myapp/myapp.conf', 
                     '~/.myapp.conf',
                     '~/.myapp/config']
    Foo => bar


    $  python myapp.py -C /path/to/another/myapp.conf
    Config Paths => ['/etc/myapp/myapp.conf', 
                     '~/.myapp.conf', 
                     '~/.myapp/config', 
                     '/path/to/another/myapp.conf']
    Foo => bar2
