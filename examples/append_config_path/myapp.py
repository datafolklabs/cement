from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose

def append_config_path(app):
    if app.pargs.config_path:
        app._meta.config_files.append(app.pargs.config_path)
        #app.config.parse_file(app.pargs.config_path)
        app._setup_config_handler()

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
