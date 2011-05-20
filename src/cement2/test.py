#!/usr/bin/env python

from cement.core.app import lay_cement
from cement.core.backend import default_config
from cement.core import hook

config = default_config('myapp')
config['base']['config_files'] = ['./test.conf', 'asdfasdfasdf.conf']
config['base']['config_handler'] = 'configobj'
config['log']['debug'] = True

app = lay_cement('myapp', defaults=config)
app.load_ext('configobj')


hook.define('myhook')

@hook.register(name='myhook', weight=99)
def my_hook_one(*args, **kw):
    print 'in my_hook_one'
        
@hook.register(name='myhook', )
def my_hook_two(*args, **kw):
    print 'in my_hook_two'

@hook.register(name='myhook', weight=-1000)
def my_hook_three(*args, **kw):
    print 'in my_hook_three'




#app.config = ConfigObjConfigHandler()
app.run()
app.config.set('base', 'johnny', 'asdfasfasdf')

app.log.info('JOHNNY')
app.log.debug('KAPLA')
#c.log.info('blah')

for i in hook.run('myhook'):
    print i

