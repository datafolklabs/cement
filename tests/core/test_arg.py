
from cement.core.arg import ArgumentHandler, ArgumentInterface

# module tests

class TestArgumentInterface:
    def test_interface(self):
        assert ArgumentInterface.Meta.interface == 'argument'


class TestArgumentHandler:
    def test_subclassing(self):
        class MyArgumentHandler(ArgumentHandler):
            class Meta:
                label = 'my_argument_handler'

            def add_argument(self, *args, **kw):
                pass

            def parse(self, *args, **kw):
                pass

        h = MyArgumentHandler()
        assert h._meta.interface == 'argument'
        assert h._meta.label == 'my_argument_handler'


# app functionality and coverage tests
