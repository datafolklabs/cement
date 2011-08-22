#!/usr/bin/env python

import sys
from cement2.core import foundation, backend, hook, controller, handler

config = backend.defaults()
config['base']['debug'] = True
config['base']['config_files'] = ['./test.conf', 'asdfasdfasdf.conf']
config['base']['config_handler'] = 'configparser'
config['base']['arg_handler'] = 'argparse'
config['base']['output_handler'] = 'yaml'

# extensions
#config['base']['extensions'].append('cement2.ext.ext_configobj')
#config['base']['extensions'].append('cement2.ext.ext_optparse')
config['base']['extensions'].append('cement2.ext.ext_yaml')

#config['base']['extensions'].append('configparser')
#config['base']['extensions'].append('logging')
#config['base']['extensions'].append('json')
#config['base']['extensions'].append('yaml')
#config['base']['extensions'].append('argparse')

app = foundation.lay_cement('myapp', defaults=config)

hook.define('myhook')

@hook.register(name='myhook', weight=99)
def my_hook_one(*args, **kw):
    return 'in my_hook_one'
        
@hook.register(name='myhook', )
def my_hook_two(*args, **kw):
    return 'in my_hook_two'

@hook.register(name='myhook', weight=-1000)
def my_hook_three(*args, **kw):
    return 'in my_hook_three'

    
class MyAppBaseController(controller.CementControllerHandler):
    class meta:
        interface = controller.IController
        label = 'base'
        description = 'myapp base controller'
        arguments = [
            ('--option1', dict(action='store_true', help="some option")), 
            ('--option2', dict(action='store', metavar='VAL')),
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
        
class SecondController(controller.CementControllerHandler):
    class meta:
        interface = controller.IController
        label = 'second'
        description = 'myapp second controller'
        stacked_on = 'base'
        arguments = [
            ('--option3', dict(action='store_true', help="some option")), 
            ('--option4', dict(action='store', metavar='VAL')),
            ]
        
        defaults = dict(foo2='bar2')

    @controller.expose(hide=True, help='default command', aliases=['2'])
    def default(self):
        print("Second Controller Default!!!!!")

class ThirdController(controller.CementControllerHandler):
    class meta:
        interface = controller.IController
        label = 'third'
        description = 'myapp third controller'
        arguments = [
            ('--option5', dict(action='store_true', help="some option")), 
            ('--option6', dict(action='store', metavar='VAL')),
            ]
        
        defaults = dict(foo3='bar3')

    @controller.expose(hide=True, help='default command', aliases=['2'])
    def default(self):
        print("Third Controller Default!!!!!")

            
handler.register(MyAppBaseController)
handler.register(SecondController)
handler.register(ThirdController)
app.setup()
app.run()
