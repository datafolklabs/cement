#!/usr/bin/env python

import sys
from cement2.core import foundation, backend, hook

config = backend.defaults()
config['base']['config_files'] = ['./test.conf', 'asdfasdfasdf.conf']
config['base']['config_handler'] = 'configobj'
config['base']['arg_handler'] = 'argparse'
config['base']['output_handler'] = 'json'

# extensions
config['base']['extensions'].append('cement2.ext.ext_configobj')
config['base']['extensions'].append('cement2.ext.ext_optparse')
config['base']['extensions'].append('cement2.ext.ext_json')

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


class MyAppBaseController(object):
    __namespace__ = 'base'
    
    def __visible__(self):
        # return all exposed commands
        pass
        
    def __hidden__(self):
        # return all hidden commands
        pass
        
    def _hidden_cmd(self):
        print "in hidden-cmd"
        
    def cmd1(self):
        print 'in cmd1'

#app.controllers.append()


#app.config = ConfigObjConfigHandler()
app.setup()

app.argv = sys.argv[1:]
app.add_arg('-t', dest='t', action='store', help='t var')
app.args.add_argument('-s', '--status', dest='status', action='store', help='status option', metavar='S')
app.run()
print app.args.parsed_args.debug
print app.pargs

for i in hook.run('myhook'):
    pass

print app.render(dict(foo='bar'))
#print app.extension.loaded_extensions