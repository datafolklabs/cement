Quick Start
===========

The following outlines creating a sample 'helloworld' application.

*helloworld.py*

.. code-block:: python

    from cement.core import foundation
    
    app = foundation.CementApp('helloworld')
    try:
        app.setup()
        app.run()
        print('Hello World')
    finally:
        app.close()

Executing the application:

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
    2012-07-13 02:21:25,094 (DEBUG) cement.core.foundation : laying cement for the 'helloworld' application
    2012-07-13 02:21:25,094 (DEBUG) cement.core.hook : defining hook 'pre_setup'
    2012-07-13 02:21:25,094 (DEBUG) cement.core.hook : defining hook 'post_setup'
    2012-07-13 02:21:25,094 (DEBUG) cement.core.hook : defining hook 'pre_run'
    2012-07-13 02:21:25,094 (DEBUG) cement.core.hook : defining hook 'post_run'
    2012-07-13 02:21:25,094 (DEBUG) cement.core.hook : defining hook 'pre_close'
    2012-07-13 02:21:25,095 (DEBUG) cement.core.hook : defining hook 'post_close'
    2012-07-13 02:21:25,095 (DEBUG) cement.core.hook : defining hook 'signal'
    2012-07-13 02:21:25,095 (DEBUG) cement.core.hook : defining hook 'pre_render'
    2012-07-13 02:21:25,095 (DEBUG) cement.core.hook : defining hook 'post_render'
    2012-07-13 02:21:25,095 (DEBUG) cement.core.handler : defining handler type 'extension' (IExtension)
    2012-07-13 02:21:25,095 (DEBUG) cement.core.handler : defining handler type 'log' (ILog)
    2012-07-13 02:21:25,095 (DEBUG) cement.core.handler : defining handler type 'config' (IConfig)
    2012-07-13 02:21:25,095 (DEBUG) cement.core.handler : defining handler type 'plugin' (IPlugin)
    2012-07-13 02:21:25,095 (DEBUG) cement.core.handler : defining handler type 'output' (IOutput)
    2012-07-13 02:21:25,095 (DEBUG) cement.core.handler : defining handler type 'argument' (IArgument)
    2012-07-13 02:21:25,096 (DEBUG) cement.core.handler : defining handler type 'controller' (IController)
    2012-07-13 02:21:25,096 (DEBUG) cement.core.handler : defining handler type 'cache' (ICache)
    2012-07-13 02:21:25,096 (DEBUG) cement.core.handler : registering handler '<class 'cement.core.extension.CementExtensionHandler'>' into handlers['extension']['cement']
    2012-07-13 02:21:25,096 (DEBUG) cement.core.foundation : now setting up the 'helloworld' application
    2012-07-13 02:21:25,096 (DEBUG) cement.core.foundation : adding signal handler for signal 15
    2012-07-13 02:21:25,096 (DEBUG) cement.core.foundation : adding signal handler for signal 2
    2012-07-13 02:21:25,096 (DEBUG) cement.core.foundation : setting up helloworld.extension handler
    2012-07-13 02:21:25,097 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_nulloutput' framework extension
    2012-07-13 02:21:25,097 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_nulloutput.NullOutputHandler'>' into handlers['output']['null']
    2012-07-13 02:21:25,097 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_plugin' framework extension
    2012-07-13 02:21:25,097 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_plugin.CementPluginHandler'>' into handlers['plugin']['cement']
    2012-07-13 02:21:25,097 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_configparser' framework extension
    2012-07-13 02:21:25,098 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_configparser.ConfigParserConfigHandler'>' into handlers['config']['configparser']
    2012-07-13 02:21:25,098 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_logging' framework extension
    2012-07-13 02:21:25,098 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_logging.LoggingLogHandler'>' into handlers['log']['logging']
    2012-07-13 02:21:25,098 (DEBUG) cement.core.extension : loading the 'cement.ext.ext_argparse' framework extension
    2012-07-13 02:21:25,099 (DEBUG) cement.core.handler : registering handler '<class 'cement.ext.ext_argparse.ArgParseArgumentHandler'>' into handlers['argument']['argparse']
    2012-07-13 02:21:25,100 (DEBUG) cement.core.foundation : setting up helloworld.config handler
    2012-07-13 02:21:25,100 (DEBUG) cement.ext.ext_configparser : config file '/etc/helloworld/helloworld.conf' does not exist, skipping...
    2012-07-13 02:21:25,100 (DEBUG) cement.ext.ext_configparser : config file '/Users/derks/.helloworld.conf' does not exist, skipping...
    2012-07-13 02:21:25,100 (DEBUG) cement.core.foundation : no cache handler defined, skipping.
    2012-07-13 02:21:25,100 (DEBUG) cement.core.foundation : setting up helloworld.log handler
    2012-07-13 02:21:25,101 (DEBUG) cement.core.handler : merging config defaults from '<cement.ext.ext_logging.LoggingLogHandler object at 0x100588dd0>'
    2012-07-13 02:21:25,101 (DEBUG) helloworld : logging initialized for 'helloworld' using LoggingLogHandler
    2012-07-13 02:21:25,101 (DEBUG) cement.core.foundation : setting up helloworld.plugin handler
    2012-07-13 02:21:25,102 (DEBUG) cement.ext.ext_plugin : plugin config dir /etc/helloworld/plugins.d does not exist.
    2012-07-13 02:21:25,102 (DEBUG) cement.core.foundation : setting up helloworld.arg handler
    2012-07-13 02:21:25,103 (DEBUG) cement.core.foundation : setting up helloworld.output handler
    2012-07-13 02:21:25,103 (DEBUG) cement.core.foundation : setting up application controllers
    2012-07-13 02:21:25,103 (DEBUG) cement.core.foundation : no controller could be found.
    Hello World
    2012-07-13 02:21:25,103 (DEBUG) cement.core.foundation : closing the application


Damn son, WTF?  Don't worry, we'll explain everything in the rest of the doc.

Getting Warmer
--------------

The following is a more advanced example that showcases some of the default
application features.  Notice the creation of command line arguments, default
config creation, and logging.

*myapp.py*

.. code-block:: python
    
    from cement.core import backend, foundation, hook

    # set default config options
    defaults = backend.defaults('myapp')
    defaults['myapp']['debug'] = False
    defaults['myapp']['foo'] = 'bar'

    # create an application
    app = foundation.CementApp('myapp', config_defaults=defaults)

    # register any framework hook functions after app creation, and before 
    # app.setup()
    def my_hook(app):
        assert app.config.has_key('myapp', 'foo')

    hook.register('post_setup', my_hook)
    
    try:
        # setup the application
        app.setup()

        # add arguments
        app.args.add_argument('-f', '--foo', action='store', metavar='STR',
                              help='the notorious foo option')
        app.log.debug("About to run my myapp application!")
        app.run()

        # add application logic
        if app.pargs.foo:
            app.log.info("Received the 'foo' option with value '%s'." % app.pargs.foo)
        else:
            app.log.warn("Did not receive a value for 'foo' option.")

    finally:
        # close the application
        app.close()
        
And execution:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py [-h] [--debug] [--quiet] [-f STR]

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f STR, --foo STR  the notorious foo option
    
    $ python myapp.py --foo=bar
    INFO: Received the 'foo' option with value 'bar'.


Diving Right In
---------------

This final example demonstrates the use of application controllers that 
handle command dispatch and rapid development.

*myapp.py*

.. code-block:: python

    from cement.core import backend, foundation, controller, handler

    # define an application base controller
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            label = 'base'
            description = "My Application does amazing things!"

            config_defaults = dict(
                foo='bar',
                some_other_option='my default value',
                )
        
            arguments = [
                (['-f', '--foo'], dict(action='store', help='the notorious foo option')),
                (['-C'], dict(action='store_true', help='the big C option'))
                ]
    
        @controller.expose(hide=True, aliases=['run'])
        def default(self):
            self.log.info('Inside base.default function.')
            if self.pargs.foo:
                self.log.info("Recieved option 'foo' with value '%s'." % \
                              self.pargs.foo)
                      
        @controller.expose(help="this command does relatively nothing useful.")
        def command1(self):
            self.log.info("Inside base.command1 function.")
    
        @controller.expose(aliases=['cmd2'], help="more of nothing.")
        def command2(self):
            self.log.info("Inside base.command2 function.")

    # define a second controller
    class MySecondController(controller.CementBaseController):
        class Meta:
            label = 'secondary'
            stacked_on = 'base'
        
        @controller.expose(help='this is some command', aliases=['some-cmd'])
        def some_other_command(self):
            pass
        
    class MyApp(foundation.CementApp):
        class Meta:
            label = 'helloworld'
            base_controller = MyAppBaseController

    # create the app      
    app = MyApp()
  
    # Register any handlers that aren't passed directly to CementApp
    handler.register(MySecondController)

    try:
        # setup the application
        app.setup()
    
        # run the application
        app.run()
    finally:
        # close the app
        app.close()

As you can see, we're able to build out the core functionality of our app such
as arguments and sub-commands via controller classes.

Lets see what this looks like:

.. code-block:: text

    $ python myapp.py --help
    usage: myapp.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    My Application does amazing things!

    commands:

      command1
        this command does relatively nothing useful.

      command2 (aliases: cmd2)
        more of nothing.

      some-other-command (aliases: some-cmd)
        this is some command

    optional arguments:
      -h, --help         show this help message and exit
      --debug            toggle debug output
      --quiet            suppress all output
      -f FOO, --foo FOO  the notorious foo option
      -C                 the big C option      
      
    $ python myapp.py command1
    INFO: Inside base.command1 function.
      
    $ python myapp.py command2
    INFO: Inside base.command2 function.
    
    $ python myapp.py cmd2
    INFO: Inside base.command2 function.    
