
from cement import init_config, CementApp

config = init_config()
config['app_name'] = 'test'
config['log_to_console'] = True 
c = CementApp(config)
c.log.info('blah')

