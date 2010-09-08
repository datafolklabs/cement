
from cement.core.hook import define_hook, register_hook
from cement.core.namespace import CementNamespace, register_namespace

define_hook('my_example_hook')

# Setup the 'example' namespace object
example = CementNamespace(
            label='example', 
            controller='ExampleController',
            description='Example Plugin for cementtest',
            required_api='0.7-0.8:20100210',
            provider='cementtest'
            )
example.config['foo'] = 'bar'
example.options.add_option('-F', '--foo', action='store',
    dest='foo', default=None, help='Example Foo Option'
    )

register_namespace(example)

@register_hook(weight=99)
def my_example_hook():
    return 99

@register_hook(name='my_example_hook')
def some_other_hook_name():
    return 0

@register_hook(weight=-100)
def my_example_hook():
    return -100



