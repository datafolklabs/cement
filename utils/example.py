
from cement2.core import backend, foundation, hook

# set default config options
defaults = backend.defaults()
defaults['base']['debug'] = False
defaults['base']['foo'] = 'bar'

# create an application
app = foundation.lay_cement('example', defaults=defaults)

# register any framework hook functions after app creation, and before 
# app.setup()
@hook.register()
def cement_validate_config_hook(config):
    assert config.has_key('base', 'foo')
    
# setup the application
app.setup()

# add arguments
app.args.add_argument('--foo', action='store', metavar='STR',
                      help='the notorious foo option')

# run the application
app.log.debug("About to run my example application!")
app.run()

# add application logic
if app.pargs.foo:
    app.log.info("Received the 'foo' option with value '%s'." % app.pargs.foo)
else:
    app.log.warn("Did not receive a value for 'foo' option.")
    