Load Extensions Via a Configuration File
========================================

Some use cases require that end-users are able to modify what framework
extensions are loaded via a configuration file.  The following gives an
example of how an application can support an optional ``extensions``
configuration setting that will **append** extensions to
``CementApp.Meta.extensions``.

Note that extensions loaded in this way will happen **after** application
setup (when ``app.setup()`` is called).  Normally, extensions are loaded
just before the configuration files are read.  Therefore, some extensions
may not be compatible with this method if they attempt to perform any actions
before ``app.setup()`` completes (such as in early framework hooks).

**myapp.py**

.. code-block:: python

    from cement.core.foundation import CementApp

    class MyApp(CementApp):
        class Meta:
            label = 'myapp'

        def validate_config(self):
            if 'extensions' in self.config.keys('myapp'):
                exts = self.config.get('myapp', 'extensions')

                # convert a comma-separated string to a list
                if type(exts) is str:
                    ext_list = exts.split(',')

                    # clean up extra space if they had it inbetween commas
                    ext_list = (x.strip() for x in ext_list)

                    # set the new extensions value in the config
                    self.config.set('myapp', 'extensions', ext_list)

                # otherwise, if it's a list (ConfigObj?)
                elif type(exts) is list:
                    ext_list = exts

                for ext in ext_list:
                    # load the extension
                    self.ext.load_extension(ext)

                    # add to meta data
                    self._meta.extensions.append(ext)

    app = MyApp()
    try:
        app.setup()
        app.run()
    finally:
        app.close()

**myapp.conf**

.. code-block:: text

    [myapp]
    extensions = json, yaml


Which looks like:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    MyApp Does Amazing Things

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      --json      toggle json output handler
      --yaml      toggle yaml output handler


Note the ``--json`` and ``--yaml`` configuration options that are provided
by the loaded extensions.
