Quick Start
===========

The following creates and runs a sample 'helloworld' application.

*helloworld.py*

.. code-block:: python

    from cement.core.foundation import CementApp

    with CementApp('helloworld') as app:
        app.run()
        print('Hello World')


The above is equivalent to (should you need more control over setup and
closing an application):

.. code-block:: python

    from cement.core.foundation import CementApp

    app = CementApp('helloworld')
    app.setup()
    app.run()
    print('Hello World')
    app.close()


Running the application looks like:

.. code-block:: text

    $ python helloworld.py
    Hello World


Oh, I can just here you saying, "Whoa whoa... hang on a minute.  This is a joke
right, all you did was print 'Hello World' to STDOUT.  What kind of framework
is this?".  Well obviously this is just an introduction to show that the
creation of an application is dead simple.  Lets take a look further:

.. code-block:: text

    $ python helloworld.py --help
    usage: helloworld.py [-h] [--debug] [--quiet]

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output


Oh nice, ok... ArgParse is already setup with a few options I see.  What else?

.. code-block:: text

    $ python helloworld.py --debug
    2014-04-15 12:28:24,705 (DEBUG) cement.core.foundation : laying cement for the 'helloworld' application
    2014-04-15 12:28:24,705 (DEBUG) cement.core.hook : defining hook 'pre_setup'
    2014-04-15 12:28:24,705 (DEBUG) cement.core.hook : defining hook 'post_setup'
    2014-04-15 12:28:24,705 (DEBUG) cement.core.hook : defining hook 'pre_run'
    2014-04-15 12:28:24,705 (DEBUG) cement.core.hook : defining hook 'post_run'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.hook : defining hook 'pre_argument_parsing'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.hook : defining hook 'post_argument_parsing'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.hook : defining hook 'pre_close'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.hook : defining hook 'post_close'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.hook : defining hook 'signal'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.hook : defining hook 'pre_render'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.hook : defining hook 'post_render'
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'extension' (IExtension)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'log' (ILog)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'config' (IConfig)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'plugin' (IPlugin)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'output' (IOutput)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'argument' (IArgument)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'controller' (IController)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : defining handler type 'cache' (ICache)
    2014-04-15 12:28:24,706 (DEBUG) cement.core.handler : registering handler '<class 'cement.core.extension.CementExtensionHandler'>' into handlers['extension']['cement']
    2014-04-15 12:28:24,706 (DEBUG) cement.core.foundation : now setting up the 'helloworld' application
    2014-04-15 12:28:24,706 (DEBUG) cement.core.foundation : adding signal handler for signal 15
    2014-04-15 12:28:24,712 (DEBUG) cement.core.foundation : adding signal handler for signal 2
    2014-04-15 12:28:24,712 (DEBUG) cement.core.foundation : setting up helloworld.extension handler
    2014-04-15 12:28:24,712 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_dummy' framework extension
    2014-04-15 12:28:24,712 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_dummy.DummyOutputHandler'>' into handlers['output']['null']
    2014-04-15 12:28:24,712 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_plugin' framework extension
    2014-04-15 12:28:24,713 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_plugin.CementPluginHandler'>' into handlers['plugin']['cement']
    2014-04-15 12:28:24,713 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_configparser' framework extension
    2014-04-15 12:28:24,713 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_configparser.ConfigParserConfigHandler'>' into handlers['config']['configparser']
    2014-04-15 12:28:24,713 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_logging' framework extension
    2014-04-15 12:28:24,713 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_logging.LoggingLogHandler'>' into handlers['log']['logging']
    2014-04-15 12:28:24,713 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_argparse' framework extension
    2014-04-15 12:28:24,714 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_argparse.ArgParseArgumentHandler'>' into handlers['argument']['argparse']
    2014-04-15 12:28:24,714 (DEBUG) cement.core.foundation : setting up helloworld.config handler
    2014-04-15 12:28:24,714 (DEBUG) cement.ext.ext_configparser : config file '/etc/helloworld/helloworld.conf' does not exist, skipping...
    2014-04-15 12:28:24,714 (DEBUG) cement.ext.ext_configparser : config file '/Users/derks/.helloworld/config' does not exist, skipping...
    2014-04-15 12:28:24,715 (DEBUG) cement.core.foundation : no cache handler defined, skipping.
    2014-04-15 12:28:24,715 (DEBUG) cement.core.foundation : setting up helloworld.log handler
    2014-04-15 12:28:24,715 (DEBUG) cement.core.handler : merging config defaults from '<cement.ext.ext_logging.LoggingLogHandler object at 0x1015c4ed0>' into section 'log.logging'
    2014-04-15 12:28:24,715 (DEBUG) helloworld:None : logging initialized for 'helloworld:None' using LoggingLogHandler
    2014-04-15 12:28:24,715 (DEBUG) cement.core.foundation : setting up helloworld.plugin handler
    2014-04-15 12:28:24,715 (DEBUG) cement.ext.ext_plugin : plugin config dir /Users/derks/Development/boss/tmp/helloworld/config/plugins.d does not exist.
    2014-04-15 12:28:24,716 (DEBUG) cement.core.foundation : setting up helloworld.arg handler
    2014-04-15 12:28:24,716 (DEBUG) cement.core.foundation : setting up helloworld.output handler
    2014-04-15 12:28:24,716 (DEBUG) cement.core.foundation : setting up application controllers
    Hello World
    2014-04-15 12:28:24,716 (DEBUG) cement.core.foundation : closing the application


Damn son, WTF?  Don't worry, we'll explain everything in the rest of the doc.

Getting Warmer
--------------

The following is a more advanced example that showcases some of the default
application features.  Notice the creation of command line arguments, default
config creation, and logging.

*myapp.py*

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core import hook
    from cement.utils.misc import init_defaults

    # define our default configuration options
    defaults = init_defaults('myapp')
    defaults['myapp']['debug'] = False
    defaults['myapp']['some_param'] = 'some value'

    # define any hook functions here
    def my_cleanup_hook(app):
        pass

    # define the application class
    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            config_defaults = defaults
            extensions = ['daemon', 'memcached', 'json', 'yaml']
            hooks = [
                ('pre_close', my_cleanup_hook),
            ]

    with MyApp() as app:
        # add arguments to the parser
        app.args.add_argument('-f', '--foo', action='store', metavar='STR',
                              help='the notorious foo option')

        # log stuff
        app.log.debug("About to run my myapp application!")

        # run the application
        app.run()

        # continue with additional application logic
        if app.pargs.foo:
            app.log.info("Received option: foo => %s" % app.pargs.foo)


And execution:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f STR, --foo STR  the notorious foo option

    $ python myapp.py --foo=bar
    INFO: Received option: foo => bar


Diving Right In
---------------

This final example demonstrates the use of application controllers that
handle command dispatch and rapid development.

*myapp.py*

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose

    class MyBaseController(CementBaseController):
        class Meta:
            label = 'base'
            description = "My Application does amazing things!"
            arguments = [
                ( ['-f', '--foo'],
                  dict(action='store', help='the notorious foo option') ),
                ( ['-C'],
                  dict(action='store_true', help='the big C option') ),
                ]

        @expose(hide=True)
        def default(self):
            self.app.log.info('Inside MyBaseController.default()')
            if self.app.pargs.foo:
                print("Recieved option: foo => %s" % self.app.pargs.foo)

        @expose(help="this command does relatively nothing useful")
        def command1(self):
            self.app.log.info("Inside MyBaseController.command1()")

        @expose(aliases=['cmd2'], help="more of nothing")
        def command2(self):
            self.app.log.info("Inside MyBaseController.command2()")


    class MySecondController(CementBaseController):
        class Meta:
            label = 'second'
            stacked_on = 'base'

        @expose(help='this is some command', aliases=['some-cmd'])
        def second_cmd1(self):
            self.app.log.info("Inside MySecondController.second_cmd1")


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            base_controller = 'base'
            handlers = [MyBaseController, MySecondController]



    with MyApp() as app:
        app.run()


As you can see, we're able to build out the core functionality of our app such
as arguments and sub-commands via controller classes.

Lets see what this looks like:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py (sub-commands ...) [options ...] {arguments ...}

    My Application does amazing things!

    commands:

      command1
        this command does relatively nothing useful

      command2 (aliases: cmd2)
        more of nothing

      second-cmd1 (aliases: some-cmd)
        this is some command

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f FOO, --foo FOO  the notorious foo option
      -C                 the big C option

    $ python myapp.py
    INFO: Inside MyBaseController.default()

    $ python myapp.py command1
    INFO: Inside MyBaseController.command1()

    $ python myapp.py command2
    INFO: Inside MyBaseController.command2()

    $ python myapp.py second-cmd1
    INFO: Inside MySecondController.second_cmd1()
