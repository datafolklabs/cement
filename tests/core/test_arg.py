
from cement.core.arg import ArgumentInterface, ArgumentHandler


# module tests

class TestArgumentInterface(object):
    def test_interface(self):
        assert ArgumentInterface.Meta.interface == 'argument'


class TestArgumentHandler(object):
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
