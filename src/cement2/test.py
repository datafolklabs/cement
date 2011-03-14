
from zope import interface
from cement import CementApp
from cement.core.app import lay_cement
from cement.core.backend import get_defaults
from cement.core.handler import register_handler, get_handler
from cement.handlers.config import IConfigHandler, ConfigObjConfigHandler
        
defaults = get_defaults('myapp')
defaults['base']['config_files'] = ['./test.conf', 'asdfasdfasdf.conf']
defaults['base']['config_handler'] = 'configobj'

app = lay_cement('myapp', defaults=defaults)

register_handler(ConfigObjConfigHandler)

app.config = ConfigObjConfigHandler()
#app.config.merge(defaults)

#c = CementApp('myapp', 
#        default_config=config,
#        config_handler=get_handler('config', 'configobj')(),
#        )




app.run()
print app.config
print app.config.get('base', 'foo')
print app.config.get('section2', 'a')


#c.log.info('blah')


