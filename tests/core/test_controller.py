
from cement.core.controller import ControllerInterface, ControllerHandler


# module tests

class TestControllerInterface(object):
    def test_interface(self):
        assert ControllerInterface.Meta.interface == 'controller'


class TestControllerHandler(object):
    def test_subclassing(self):
        class MyControllerHandler(ControllerHandler):
            class Meta:
                label = 'my_controller_handler'

            def _dispatch(self, *args, **kw):
                pass

        h = MyControllerHandler()
        assert h._meta.interface == 'controller'
        assert h._meta.label == 'my_controller_handler'

# app functionality and coverage tests
