
from cement import CementApp
from cement.core.backend import init_config

config = init_config()
config['config_files'] = ['./test.conf']

c = CementApp('myapp', default_config=config)
c.run()

print c.config.get('base', 'foo')
print c.config.get('section2', 'a')
print c.config

c.log.info('blah')


