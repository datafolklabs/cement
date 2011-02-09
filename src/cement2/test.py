
from cement import CementApp
from cement.core.backend import init_config

config = init_config()
config['config_files'] = ['./test.conf']

c = CementApp('myapp', default_config=config)
c.run()
print c.config.get('base', 'foo')

c.log.info('blah')


