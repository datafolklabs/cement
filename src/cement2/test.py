#!/usr/bin/env python

from cement.core import app, backend, hook

config = backend.default_config('myapp')
config['base']['config_files'] = ['./test.conf', 'asdfasdfasdf.conf']
config['base']['config_handler'] = 'configobj'
config['base']['output_handler'] = 'json'
config['log']['debug'] = True

base = app.lay_cement('myapp', defaults=config)
base.load_ext('configobj')
base.load_ext('json')

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
base.run()
base.config.set('base', 'johnny', 'asdfasfasdf')

base.log.info('JOHNNY')
base.log.debug('KAPLA')
print base.output
#c.log.info('blah')

for i in hook.run('myhook'):
    print i

print base.output.render(dict(foo='bar'))