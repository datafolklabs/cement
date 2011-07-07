
from cement2.core import foundation, backend

defaults = backend.defaults()
defaults['base']['config_handler'] = 'configobj'
defaults['base']['extensions'] = [
    'configobj',
    'json',
    'logging',
    'argparse',
    ]
app = foundation.lay_cement('helloworld', defaults=defaults)
app.setup()
app.run()

