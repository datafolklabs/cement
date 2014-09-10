"""Tests for cement.ext.ext_smtp."""

from cement.utils import test
from cement.utils.misc import rando, init_defaults

APP = "app-%s" % rando()[:12]


class SMTPMailHandlerTestCase(test.CementTestCase):
    def setUp(self):
        super(SMTPMailHandlerTestCase, self).setUp()
        self.app = self.make_app(APP,
            extensions=['smtp'],
            mail_handler='smtp',
            argv=[],
            )

    def test_smtp_defaults(self):
        defaults = init_defaults(APP, 'mail.smtp')
        defaults['mail.smtp']['to'] = 'nobody@localhost'
        defaults['mail.smtp']['from_addr'] = 'nobody@localhost'
        defaults['mail.smtp']['cc'] = 'nobody@localhost'
        defaults['mail.smtp']['bcc'] = 'nobody@localhost'
        defaults['mail.smtp']['subject'] = 'Test Email To nobody@localhost'
        defaults['mail.smtp']['subject_prefix'] = 'PREFIX >'

        self.app = self.make_app(APP,
            config_defaults=defaults,
            extensions=['smtp'],
            mail_handler='smtp',
            argv=[],
            )
        self.app.setup()
        self.app.run()
        self.app.mail.send('TEST MESSAGE')

