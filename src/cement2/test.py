#!/usr/bin/env python

import sys
from cement2.core import foundation, backend, hook, controller, handler

app = foundation.lay_cement('myapp')

class MyAppBaseController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'base'
        description = 'myapp base controller'
        arguments = [
            (['--option1'], dict(action='store_true', help="some option")), 
            (['--option2'], dict(action='store', metavar='VAL')),
            ]
        
        defaults = dict(foo='bar')

    @controller.expose(hide=False, help='default command', aliases=['run'])
    def default(self):
        print("Hello World!!!!!")
        
    @controller.expose(hide=True, help='cmd1 help info')
    def cmd_help(self):
        print("in hidden-cmd")
    
    @controller.expose(help='cmd1 does awesome things')
    def cmd(self):
        print('in cmd1')
        
class SecondController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'second'
        description = 'myapp second controller'
        stacked_on = 'base'
        arguments = [
            (['--option3'], dict(action='store', metavar='VAL')), 
            (['--option4'], dict(action='store', metavar='VAL')),
            ]
        
        defaults = dict(foo2='bar2')
    
    @controller.expose()
    def cmd2():
        pass
        
class ThirdController(controller.CementBaseController):
    class meta:
        interface = controller.IController
        label = 'third'
        description = 'myapp third controller'
        arguments = [
            (['--option5'], dict(action='store_true', help="some option")), 
            (['--option6'], dict(action='store', metavar='VAL')),
            ]
        
        defaults = dict(foo3='bar3')

    @controller.expose(hide=True, help='default command', aliases=['cmd'])
    def default(self):
        print("Third Controller Default!!!!!")

    @controller.expose(help='cmd3 does awesome things')
    def cmd3(self):
        print('in cmd3')
            
handler.register(MyAppBaseController)
handler.register(SecondController)
handler.register(ThirdController)
app.setup()
app.run()
