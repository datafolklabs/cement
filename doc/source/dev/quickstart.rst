Quick Start
===========

The following outlines installation of Cement2, as well as quick starting a
new 'helloworld' application.

Development Environment
-----------------------

It is recommended to work out of a `VirtualENV <http://pypi.python.org/pypi/virtualenv>`_ 
for development, which is reference throughout this documentation.  VirtualENV
is easily installed on most platforms either with 'easy_install' or 'pip' or
via your OS distributions packaging system (yum, apt, brew, etc).


Installing From Git
-------------------

Currently, the 'master' branch is the current stable version of cement (0.8.x).
To install Cement2 you need to checkout the 'portland' branch which is the
source for development of the next major version of Cement.  

.. code-block:: text

    $ git clone git://github.com/derks/cement.git
    
    $ cd cement
    
    $ git checkout --track -b portland origin/portland
    Branch portland set up to track remote branch portland from origin.
    Switched to a new branch 'portland'

    $ virtualenv --no-site-packages ~/env/helloworld/
    
    $ source ~/env/helloworld/bin/activate
    
    (helloworld) $ cd src/cement2/
    
    (helloworld) $ python setup.py install
    

To run tests, do the following from the 'root' directory:

.. code-block:: text
    
    (helloworld) $ pip install nose
    
    (helloworld) $ ./utils/run_tests.sh


A Simple Hello World Application
--------------------------------

The following is a bare minimum 'helloworld' application.

.. code-block:: python

    from cement2.core import foundation
    
    try:
        app = foundation.CementApp('helloworld')
        app.setup()
        app.run()
        print('Hello World')
    finally:
        app.close()
    
And execution:

.. code-block:: text

    $ python helloworld.py 
    Hello World
    
    
Oh, I can here you saying, "Whoa whoa... hang on a minute.  This is a joke 
right, all you did was print 'Hello World' to stdout.  What kind of framework 
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
    2011-11-15 15:19:35,157 (DEBUG) cement2.core.foundation : laying cement for the 'helloworld' application
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.hook : defining hook 'cement_pre_setup_hook'
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.hook : defining hook 'cement_post_setup_hook'
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.hook : defining hook 'cement_pre_run_hook'
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.hook : defining hook 'cement_post_run_hook'
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.hook : defining hook 'cement_on_close_hook'
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.handler : defining handler type 'extension' (IExtension)
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.handler : defining handler type 'log' (ILog)
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.handler : defining handler type 'config' (IConfig)
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.handler : defining handler type 'plugin' (IPlugin)
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.handler : defining handler type 'output' (IOutput)
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.handler : defining handler type 'argument' (IArgument)
    2011-11-15 15:19:35,158 (DEBUG) cement2.core.handler : defining handler type 'controller' (IController)
    2011-11-15 15:19:35,159 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.core.extension.CementExtensionHandler'>' into handlers['extension']['cement']
    2011-11-15 15:19:35,159 (DEBUG) cement2.core.foundation : now setting up the 'helloworld' application
    2011-11-15 15:19:35,159 (DEBUG) cement2.core.foundation : setting up helloworld.extension handler
    2011-11-15 15:19:35,159 (DEBUG) cement2.core.foundation : no config defaults from '<cement2.core.extension.CementExtensionHandler object at 0x1005b2e10>'
    2011-11-15 15:19:35,159 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_nulloutput' framework extension
    2011-11-15 15:19:35,159 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.lib.ext_nulloutput.NullOutputHandler'>' into handlers['output']['null']
    2011-11-15 15:19:35,160 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_plugin' framework extension
    2011-11-15 15:19:35,161 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.lib.ext_plugin.CementPluginHandler'>' into handlers['plugin']['cement']
    2011-11-15 15:19:35,161 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_configparser' framework extension
    2011-11-15 15:19:35,164 (DEBUG) cement2.core.handler : registering handler 'cement2.lib.ext_configparser.ConfigParserConfigHandler' into handlers['config']['configparser']
    2011-11-15 15:19:35,164 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_logging' framework extension
    2011-11-15 15:19:35,165 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.lib.ext_logging.LoggingLogHandler'>' into handlers['log']['logging']
    2011-11-15 15:19:35,165 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_argparse' framework extension
    2011-11-15 15:19:35,165 (DEBUG) cement2.core.handler : registering handler '<class 'cement2.lib.ext_argparse.ArgParseArgumentHandler'>' into handlers['argument']['argparse']
    2011-11-15 15:19:35,165 (DEBUG) cement2.core.foundation : setting up helloworld.config handler
    2011-11-15 15:19:35,166 (DEBUG) cement2.lib.ext_configparser : config file '/etc/helloworld/helloworld.conf' does not exist, skipping...
    2011-11-15 15:19:35,166 (DEBUG) cement2.lib.ext_configparser : config file '/Users/wdierkes/.helloworld.conf' does not exist, skipping...
    2011-11-15 15:19:35,166 (DEBUG) cement2.core.foundation : validating required configuration parameters
    2011-11-15 15:19:35,166 (DEBUG) cement2.core.foundation : setting up helloworld.log handler
    2011-11-15 15:19:35,166 (DEBUG) cement2.core.foundation : setting config defaults from '<cement2.lib.ext_logging.LoggingLogHandler object at 0x100419050>'
    2011-11-15 15:19:35,167 (DEBUG) helloworld : logging initialized for 'helloworld' using LoggingLogHandler
    2011-11-15 15:19:35,167 (DEBUG) cement2.core.foundation : setting up helloworld.plugin handler
    2011-11-15 15:19:35,167 (DEBUG) cement2.core.foundation : no config defaults from '<cement2.lib.ext_plugin.CementPluginHandler object at 0x1005c9890>'
    2011-11-15 15:19:35,167 (DEBUG) cement2.lib.ext_plugin : plugin config dir /etc/helloworld/plugins.d does not exist.
    2011-11-15 15:19:35,167 (DEBUG) cement2.core.foundation : setting up helloworld.arg handler
    2011-11-15 15:19:35,169 (DEBUG) cement2.core.foundation : no config defaults from 'ArgParseArgumentHandler(prog='test.py', usage=None, description=None, version=None, formatter_class=<class 'argparse.HelpFormatter'>, conflict_handler='error', add_help=True)'
    2011-11-15 15:19:35,169 (DEBUG) cement2.core.foundation : setting up helloworld.output handler
    2011-11-15 15:19:35,169 (DEBUG) cement2.core.foundation : no config defaults from '<cement2.lib.ext_nulloutput.NullOutputHandler object at 0x1005c9c50>'
    2011-11-15 15:19:35,169 (DEBUG) cement2.core.foundation : setting up helloworld.controller handler
    2011-11-15 15:19:35,169 (DEBUG) cement2.core.foundation : no controller could be found.
    Hello World
    

Damn son, WTF?  Don't worry, we'll explain everything in the rest of the doc.

Getting Warmer
--------------

The following is a more advanced example that showcases some of the default
application features.

.. code-block:: python
    
    from cement2.core import backend, foundation, hook

    # set default config options
    defaults = backend.defaults('myapp')
    defaults['myapp']['debug'] = False
    defaults['myapp']['foo'] = 'bar'

    # create an application
    app = foundation.CementApp('example', config_defaults=defaults)

    # register any framework hook functions after app creation, and before 
    # app.setup()
    @hook.register()
    def cement_post_setup_hook(app):
        assert app.config.has_key('base', 'foo')
    
    # setup the application
    app.setup()

    # add arguments
    app.args.add_argument('-f', '--foo', action='store', Metavar='STR',
                          help='the notorious foo option')

    # run the application
    try:
        app.log.debug("About to run my example application!")
        app.run()

        # add application logic
        if app.pargs.foo:
            app.log.info("Received the 'foo' option with value '%s'." % app.pargs.foo)
        else:
            app.log.warn("Did not receive a value for 'foo' option.")

    finally:
        # close the application
        app.close()
    
.. code-block:: text

    $ python scripts/example.py --help
    usage: example.py [-h] [--debug] [--quiet] [--foo STR]

    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      -f, --foo STR   the notorious foo option
    
    $ python scripts/example.py --foo=bar
    INFO: Received the 'foo' option with value 'bar'.


Diving Right In
---------------

This final example demonstrates the use of application controllers that 
handle command dispatch and rapid development.

.. code-block:: python

    from cement2.core import backend, foundation, controller, handler

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

    # setup the application
    app.setup()

    try:
        # run the application
        app.run()
    finally:
        # close the application
        app.close()

As you can see, we're able to build out the core functionality of our app
via a controller class.  Lets see what this looks like:

.. code-block:: text

    $ python example2.py --help
    usage: example2.py <CMD> -opt1 --opt2=VAL [arg1] [arg2] ...

    My Application does amazing things!

    commands:

      command1
        this command does relatively nothing useful.

      command2 (aliases: cmd2)
        more of nothing.

      some-other-command (aliases: some-cmd)
        this is some command
        
    optional arguments:
      -h, --help  show this help message and exit
      --debug     toggle debug output
      --quiet     suppress all output
      -f,     --foo FOO   the notorious foo option
      -C          the big C option
      
      
    $ python example2.py 
    INFO: Inside base.default function.
    
    $ python example2.py command1
    INFO: Inside base.command1 function.
    
    $ python example2.py cmd2
    INFO: Inside base.command2 function.
    