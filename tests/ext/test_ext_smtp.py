
import mock
from cement.utils.test import TestApp
from cement.utils.misc import init_defaults


class SMTPApp(TestApp):
    class Meta:
        extensions = ['smtp']
        mail_handler = 'smtp'


def test_smtp_defaults():
    defaults = init_defaults('mail.smtp')
    defaults['mail.smtp']['to'] = 'nobody@localhost'
    defaults['mail.smtp']['from_addr'] = 'nobody@localhost'
    defaults['mail.smtp']['cc'] = 'nobody@localhost'
    defaults['mail.smtp']['bcc'] = 'nobody@localhost'
    defaults['mail.smtp']['subject'] = 'Test Email To nobody@localhost'
    defaults['mail.smtp']['subject_prefix'] = 'PREFIX >'

    with mock.patch('smtplib.SMTP') as mock_smtp:
        with SMTPApp(config_defaults=defaults) as app:
            app.run()
            app.mail.send('TEST MESSAGE')

            instance = mock_smtp.return_value
            assert instance.send_message.call_count == 1


def test_smtp_ssl_tls():
    defaults = init_defaults('mail.smtp')
    defaults['mail.smtp']['ssl'] = True
    defaults['mail.smtp']['tls'] = True
    defaults['mail.smtp']['port'] = 25

    with mock.patch('smtplib.SMTP_SSL') as mock_smtp:
        with SMTPApp(config_defaults=defaults, debug=True) as app:
            app.run()
            app.mail.send('TEST MESSAGE',
                          to=['me@localhost'],
                          from_addr='noreply@localhost')

            instance = mock_smtp.return_value
            assert instance.send_message.call_count == 1
            assert instance.starttls.call_count == 1


def test_smtp_auth(rando):
    defaults = init_defaults(rando, 'mail.smtp')
    defaults[rando]['debug'] = True
    defaults['mail.smtp']['auth'] = True
    defaults['mail.smtp']['username'] = 'john.doe'
    defaults['mail.smtp']['password'] = 'password'

    with mock.patch('smtplib.SMTP') as mock_smtp:
        with SMTPApp(config_defaults=defaults) as app:
            app.run()
            app.mail.send('TEST MESSAGE',
                          to=['me@localhost'],
                          from_addr='noreply@localhost')

            instance = mock_smtp.return_value
            assert instance.login.call_count == 1
            assert instance.send_message.call_count == 1
