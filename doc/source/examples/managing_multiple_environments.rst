Managing Multiple Environments
==============================

Many applications and use-cases call for managing multiple environments and
handling common settings between them.  These environments might refer to 
infrastructure such as ``production``, ``staging``, or ``dev``... or perhaps
it might be to handle multiple accounts or regions within an account at a 
service provider.  

The following example outlines one possible approach to managing multiple 
infrastructure accounts from an application Built on Cement:

**myapp.py**:

.. code-block:: python

    from cement.core.foundation import CementApp
    from cement.core.controller import CementBaseController, expose
    from cement.utils.misc import init_defaults

    # set default settings for our different environments
    defaults = init_defaults('myapp', 'env.production', 'env.staging', 'env.dev')
    defaults['myapp']['default_env'] = 'production'
    defaults['env.production']['foo'] = 'bar.production'
    defaults['env.staging']['foo'] = 'bar.staging'
    defaults['env.dev']['foo'] = 'bar.dev'

    # do this in a hook so that we can load the default from config
    def set_default_env(app):
        if app.pargs.env is None:
            app.pargs.env = app.config.get('myapp', 'default_env')

    class MyController(CementBaseController):
        class Meta:
            label = 'base'
            arguments = [
                (['-E', '--environment'], 
                 dict(help='environment override', 
                      action='store', 
                      nargs='?',
                      choices=['production', 'staging', 'dev'],
                      dest='env')),
                ]

        @expose(hide=True)
        def default(self):
            print('Inside MyController.default()')

            # shorten things up a bit for clarity
            env_key = self.app.pargs.env
            env = self.app.config.get_section_dict('env.%s' % env_key)

            print('Current Environment: %s' % env_key)
            print('Foo => %s' % env['foo'])


    class MyApp(CementApp):
        class Meta:
            label = 'myapp'
            config_defaults = defaults
            base_controller = MyController

    with MyApp() as app:
        app.hook.register('post_argument_parsing', set_default_env)
        app.run()


**myapp.conf**

.. code-block:: console

    [myapp]
    default_env = production

    [env.production]
    foo = bar.production

    [env.staging]
    foo = bar.staging

    [env.dev]
    foo = bar.dev


This looks like:

.. code-block:: console

    $ python myapp.py
    Inside MyController.default()
    Current Environment: production
    Foo => bar.production

    $ python myapp.py -E staging
    Inside MyController.default()
    Current Environment: staging
    Foo => bar.staging

    $ python myapp.py -E dev
    Inside MyController.default()
    Current Environment: dev
    Foo => bar.dev

The idea being that you can maintain a single set of operations, but modify
what or where those operations happen by simply toggling the configuration
section (that has the same configuration settings per environment).

