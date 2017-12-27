
from pytest import raises

from cement.core.foundation import TestApp
from cement.core.exc import FrameworkError
from cement.core.mail import MailHandlerBase, MailHandler


### module tests

class TestMailHandlerBase(object):
    def test_interface(self):
        assert MailHandlerBase.Meta.interface == 'mail'


class TestMailHandler(object):
    def test_subclassing(self):
        class MyMailHandler(MailHandler):
            class Meta:
                label = 'my_mail_handler'

            def send(self, *args, **kw):
                pass

        h = MyMailHandler()
        assert h._meta.interface == 'mail'
        assert h._meta.label == 'my_mail_handler'


### app functionality and coverage tests
