#!/usr/bin/env python

from cement2.core import foundation, backend, hook

config = backend.defaults()
config['base']['config_files'] = ['./test.conf', 'asdfasdfasdf.conf']
config['base']['extensions'] = ['configobj', 'yaml', 'json', 'example']
config['base']['config_handler'] = 'configobj'
config['base']['output_handler'] = 'json'

app = foundation.lay_cement('myapp', defaults=config)

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
print app.output
#c.log.info('blah')

for i in hook.run('myhook'):
    print i

print app.output.render(dict(foo='bar'))
