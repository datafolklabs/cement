
from cement2.core import backend, foundation, controller, handler

# create an application
app = foundation.lay_cement('example')

# define an application base controller
class MyAppBaseController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'base'
        description = "My Application does amazing things!"

        defaults = dict(
            foo='bar',
            some_other_option='my default value',
            )
            
        arguments = [
            ('--foo', dict(action='store', help='the notorious foo option')),
            ('-C', dict(action='store_true', help='the big C option'))
            ]
        
    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        self.log.info('Inside base.default function.')
        if self.pargs.foo:
            self.log.info("Recieved option 'foot' with value '%s'." % \
                          self.pargs.foo)
                          
    @controller.expose(help="this command does relatively nothing useful.")
    def command1(self):
        self.log.info("Inside base.command1 function.")
        
    @controller.expose(aliases=['cmd2'], help="more of nothing.")
    def command2(self):
        self.log.info("Inside base.command2 function.")
        
handler.register(MyAppBaseController)

# setup the application
app.setup()

# run the application
app.run()