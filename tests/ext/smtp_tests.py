"""Tests for cement.ext.ext_smtp."""

import mock
import sys
import smtplib
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

        with mock.patch('smtplib.SMTP') as mock_smtp:
            self.app = self.make_app(APP,
                                     config_defaults=defaults,
                                     extensions=['smtp'],
                                     mail_handler='smtp',
                                     argv=[],
                                     )
            self.app.setup()
            self.app.run()
            self.app.mail.send('TEST MESSAGE')

            instance = mock_smtp.return_value

            if int(sys.version[0]) >= 3:
                self.eq(instance.send_message.call_count, 1)
            else:
                self.eq(instance.sendmail.call_count, 1)

    def test_smtp_ssl_tls(self):
        defaults = init_defaults(APP, 'mail.smtp')
        defaults['mail.smtp']['ssl'] = True
        defaults['mail.smtp']['tls'] = True
        defaults['mail.smtp']['port'] = 25

        with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
            self.app = self.make_app(APP,
                                     config_defaults=defaults,
                                     extensions=['smtp'],
                                     mail_handler='smtp',
                                     argv=[],
                                     )
            self.app.setup()
            self.app.run()
            self.app.mail.send('TEST MESSAGE',
                               to=['me@localhost'],
                               from_addr='noreply@localhost',
                               )

            instance = mock_smtp.return_value

            if int(sys.version[0]) >= 3:
                self.eq(instance.send_message.call_count, 1)
            else:
                self.eq(instance.sendmail.call_count, 1)

            self.eq(instance.starttls.call_count, 1)

    def test_smtp_auth(self):
        defaults = init_defaults(APP, 'mail.smtp')
        defaults[APP]['debug'] = True
        defaults['mail.smtp']['auth'] = True
        defaults['mail.smtp']['username'] = 'john.doe'
        defaults['mail.smtp']['password'] = 'password'

        with mock.patch('smtplib.SMTP') as mock_smtp:
            self.app = self.make_app(APP,
                                     config_defaults=defaults,
                                     extensions=['smtp'],
                                     mail_handler='smtp',
                                     argv=[],
                                     )
            self.app.setup()
            self.app.run()
            self.app.mail.send('TEST MESSAGE',
                               to=['me@localhost'],
                               from_addr='noreply@localhost',
                               )

            instance = mock_smtp.return_value
            self.eq(instance.login.call_count, 1)
            
            if int(sys.version[0]) >= 3:
                self.eq(instance.send_message.call_count, 1)
            else:
                self.eq(instance.sendmail.call_count, 1)

