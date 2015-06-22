"""Tests for cement.ext.ext_dummy."""

from cement.utils import test
from cement.utils.misc import rando, init_defaults

APP = "app-%s" % rando()[:12]


class DummyOutputHandlerTestCase(test.CementTestCase):
    pass


class DummyMailHandlerTestCase(test.CementTestCase):

    def test_dummy_mail(self):
        self.app.setup()
        self.app.run()
        res = self.app.mail.send("Test",
                                 to=['me@localhost'],
                                 from_addr='me@localhost',
                                 )
        self.ok(res)

    def test_dummy_mail_with_subject_prefix(self):
        defaults = init_defaults(APP, 'mail.dummy')
        defaults['mail.dummy']['subject_prefix'] = 'TEST PREFIX'
        app = self.make_app(APP, config_defaults=defaults)
        app.setup()
        app.run()
        res = app.mail.send("Test",
                            to=['me@localhost'],
                            from_addr='me@localhost',
                            )
        self.ok(res)
