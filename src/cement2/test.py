
from cement import config
from cement.core.app import CementApp

config['app_name'] = 'test'
c = CementApp(config)
c.log.info('blah')

