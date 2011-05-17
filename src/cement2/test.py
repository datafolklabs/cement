
from cement.core.app import lay_cement
from cement.core.backend import default_config
from cement.core.handler import register_handler, get_handler


        
config = default_config()
config['base']['config_files'] = ['./test.conf', 'asdfasdfasdf.conf']
config['base']['config_handler'] = 'configparser'
config['log']['debug'] = True

app = lay_cement('myapp', defaults=config)
app.load_ext('configobj')


#app.config = ConfigObjConfigHandler()
app.run()
app.config.set('base', 'johnny', 'asdfasfasdf')

app.log.info('JOHNNY')
app.log.debug('KAPLA')
#c.log.info('blah')


