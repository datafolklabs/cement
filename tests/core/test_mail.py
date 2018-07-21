
from cement.core.mail import MailInterface, MailHandler


# module tests

class TestMailInterface(object):
    def test_interface(self):
        assert MailInterface.Meta.interface == 'mail'


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


# app functionality and coverage tests
