Daemon
======

The Daemon Framework Extension enables applications built on cement to easily
perform standard 'daemon' functions.  Features include:

    * Configurable runtime user and group
    * Adds the --daemon command line option
    * Adds app.daemonize() function to trigger daemon functionality where
      necessary (either in a cement_pre_run_hook or an application controller
      sub-command, etc).
    * Manages a pid file including cleanup on app.close()

Configuration
-------------

The daemon extension is configurable with the following config settings under
the [daemon] section.

    user    
        The user name to run the process as.  Default: os.environ['USER']
        
    group
        The group name to run the process as.  Default: The primary group of
        the 'user'.
    
    dir
        The directory to run the process in.  Default: /
        
    pid_file
        The filesystem path to store the PID (Process ID) file.  Default: None
    
    umask
        The umask value to pass to os.umask().  Default: 0
        

The configurations can be passed as defaults:

.. code-block:: python
    
    from cement2.core import foundation, backend
    
    defaults = backend.defaults('myapp', 'daemon')
    defaults['daemon']['user'] = 'myuser'
    defaults['daemon']['group'] = 'mygroup'
    defaults['daemon']['dir'] = '/var/lib/myapp/'
    defaults['daemon']['pid_file'] = '/var/run/myapp/myapp.pid'
    defaults['daemon']['umask'] = 0
    
    app = foundation.CementApp('myapp', config_defaults=defaults)
    

Additionally, an application configuration file might have a section like the
following:

.. code-block:: text

    [daemon]
    user = myuser
    group = mygroup
    dir = /var/lib/myapp/
    pid_file = /var/run/myapp/myapp.pid
    umask = 0

        
Example Usage
-------------

The following example shows how to add the ext_daemon extension, as well as
trigger daemon functionality before app.run() is called.

.. code-block:: python
    
    from time import sleep
    from cement2.core import foundation, backend

    try:    
        app = foundation.CementApp('myapp', extensions=['daemon'])
        app.setup()
        app.daemonize()
        app.run()
        
        count = 0
        while True:
            count = count + 1
            print('Iteration: %s' % count)
            sleep(10)
    finally:
        app.close()

An alternative to the above is to put app.daemonize() within a framework hook:

.. code-block:: python

    from cement2.core import hook
    
    @hook.register()
    def cement_pre_run_hook(app):
        app.daemonize()
        

Wherever the 'app' is created, the ext_daemon extension must be added to 
config['base']['extensions'].  Finally, some applications may prefer to only
daemonize certain sub-commands rather than the entire parent application.
For example:

.. code-block:: python

    from cement2.core import backend, foundation, controller, handler
    
    # create an application
    app = foundation.CementApp('myapp', extensions=['daemon'])

    # define an application base controller
    class MyAppBaseController(controller.CementBaseController):
        class Meta:
            interface = controller.IController
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

        @controller.expose(help="run the daemon command.")
        def run_forever(self):
            from time import sleep
            self.app.daemonize()
        
            count = 0
            while True:
                count = count + 1
                print(count)
                sleep(10)
            
    handler.register(MyAppBaseController)

    # setup the application
    app.setup()

    # run the application, and close
    try:
        app.run()
    finally:
        app.close()
        

Running The Daemon
------------------

By default, even after app.daemonize() is called... the application will 
continue to run in the foreground, but will still manage the pid and 
user/group switching.  To detach a process and send it to the background you
simply pass the '--daemon' option at command line.

.. code-block:: text

    $ python example.py --daemon

    $ ps -x | grep example
    37421 ??         0:00.01 python example2.py --daemon
    37452 ttys000    0:00.00 grep example
    
    
You will return to your shell, however you can see the process continues to
run.  The debug output also shows a bit more of what's happening behind the 
scenes:

.. code-block:: text

    2011-12-21 17:44:14,348 (DEBUG) cement2.core.extension : loading the 'cement2.ext.ext_daemon' framework extension
    2011-12-21 17:44:14,349 (DEBUG) cement2.core.hook : registering hook func 'cement_post_setup_hook' from cement2.ext.ext_daemon into hooks['cement_post_setup_hook']
    2011-12-21 17:44:14,349 (DEBUG) cement2.core.hook : registering hook func 'cement_on_close_hook' from cement2.ext.ext_daemon into hooks['cement_on_close_hook']
    2011-12-21 17:44:14,353 (DEBUG) cement2.core.hook : running hook 'cement_post_setup_hook' (<function cement_post_setup_hook at 0x1005bf938>) from cement2.ext.ext_daemon
    2011-12-21 17:44:14,354 (DEBUG) cement2.lib.ext_daemon : setting process uid(501) and gid(20)
    2011-12-21 17:44:14,355 (DEBUG) cement2.lib.ext_daemon : writing pid (42662) out to /Users/wdierkes/tmp/myapp.pid
    2011-12-21 17:44:14,355 (DEBUG) cement2.lib.ext_daemon : attempting to daemonize the current process
    2011-12-21 17:44:14,356 (DEBUG) cement2.lib.ext_daemon : successfully detached from first parent
    2011-12-21 17:44:14,358 (DEBUG) cement2.lib.ext_daemon : successfully detached from second parent


API Reference
-------------

.. _cement2.ext.ext_daemon:

:mod:`cement2.ext.ext_daemon`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: cement2.ext.ext_daemon
    :members:
    
.. _cement2.lib.ext_daemon:

:mod:`cement2.lib.ext_daemon`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: cement2.lib.ext_daemon
    :members:
    


