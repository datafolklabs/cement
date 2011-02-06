
from cement import init_config, CementApp

c = CementApp('myapp')
c.run()
c.log.info('blah')


