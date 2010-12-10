
from cement.core.hook import register_hook, define_hook
from cement.core.namespace import CementNamespace, register_namespace

# Setup the 'example' namespace object
example = CementNamespace(
            label='example_five', 
            controller='ExampleFiveController',
            description='Example Plugin for Cement Test',
            provider='cement_test'
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



