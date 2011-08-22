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
        namespace = 'base'
        description = 'myapp base controller'
        arguments = [
            ('--base', dict(action='store_true')), 
            ('--fuck', dict(action='store', metavar='FUCK')),
            ]
        
        defaults = dict(foo='bar')

    @controller.expose(hide=True, help='default command', aliases=['run'])
    def default(self):
        print("Hello World!!!!!")
        
    @controller.expose(hide=True, help='cmd1 help info')
    def cmd_help(self):
        print("in hidden-cmd")
    
    @controller.expose(help='cmd1 does awesome things')
    def cmd(self):
        print('in cmd1')
        
handler.register(MyAppBaseController)

#app.controllers.append()

#app.config = ConfigObjConfigHandler()
app.setup()

app.argv = sys.argv[1:]
app.add_arg('-t', dest='t', action='store', help='t var')
app.args.add_argument('-s', '--status', dest='status', action='store', help='status option', metavar='S')
app.log.info('This is my application log')

print('a')
app.run()
print('b')
print(app.config.get('base', 'foo'))
#print(app.args.parsed_args.debug)
#print(app.pargs)

for i in hook.run('myhook'):
    pass

#print(app.render(dict(foo='bar')))
#print app.extension.loaded_extensions