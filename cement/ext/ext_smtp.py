"""
Cement smtp extension module.
"""

import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..core import mail
from ..utils.misc import minimal_logger, is_true

LOG = minimal_logger(__name__)


class SMTPMailHandler(mail.MailHandler):

    """
    This class implements the :ref:`IMail <cement.core.mail>`
    interface, and is based on the `smtplib
    <http://docs.python.org/dev/library/smtplib.html>`_ standard library.

    """

    class Meta:

        """Handler meta-data."""

        #: Unique identifier for this handler
        label = 'smtp'

        #: Configuration default values
        config_defaults = {
            'to': [],
            'from_addr': 'noreply@localhost',
            'cc': [],
            'bcc': [],
            'subject': None,
            'subject_prefix': None,
            'host': 'localhost',
            'port': '25',
            'timeout': 30,
            'ssl': False,
            'tls': False,
            'auth': False,
            'username': None,
            'password': None,
        }

    def _get_params(self, **kw):
        params = dict()

        # some keyword args override configuration defaults
        for item in ['to', 'from_addr', 'cc', 'bcc', 'subject']:
            config_item = self.app.config.get(self._meta.config_section, item)
            params[item] = kw.get(item, config_item)

        # others don't
        other_params = ['ssl', 'tls', 'host', 'port', 'auth', 'username',
                        'password', 'timeout']
        for item in other_params:
            params[item] = self.app.config.get(self._meta.config_section,
                                               item)

        # also grab the subject_prefix
        params['subject_prefix'] = self.app.config.get(
            self._meta.config_section,
            'subject_prefix'
        )

        return params

    def send(self, body, **kw):
        """
        Send an email message via SMTP.  Keyword arguments override
        configuration defaults (cc, bcc, etc).

        Args:
            body: The message body to send

        Keyword Args:
            to (list): List of recipients (generally email addresses)
            from_addr (str): Address (generally email) of the sender
            cc (list): List of CC Recipients
            bcc (list): List of BCC Recipients
            subject (str): Message subject line

        Returns:
            bool:``True`` if message is sent successfully, ``False`` otherwise

        Example:

            .. code-block:: python

                # Using all configuration defaults
                app.mail.send('This is my message body')

                # Overriding configuration defaults
                app.mail.send('My message body'
                    from_addr='me@example.com',
                    to=['john@example.com'],
                    cc=['jane@example.com', 'rita@example.com'],
                    subject='This is my subject',
                    )

        """
        params = self._get_params(**kw)

        if is_true(params['ssl']):
            server = smtplib.SMTP_SSL(params['host'], params['port'],
                                      params['timeout'])
            LOG.debug("%s : initiating ssl" % self._meta.label)
            if is_true(params['tls']):
                LOG.debug("%s : initiating tls" % self._meta.label)
                server.starttls()

        else:
            server = smtplib.SMTP(params['host'], params['port'],
                                  params['timeout'])

        if is_true(params['auth']):
            server.login(params['username'], params['password'])

        if self.app.debug is True:
            server.set_debuglevel(9)

        self._send_message(server, body, **params)
        server.quit()

    def _send_message(self, server, body, **params):
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf-8')

        msg['From'] = params['from_addr']
        msg['To'] = ', '.join(params['to'])
        msg['Cc'] = ', '.join(params['cc'])
        msg['Bcc'] = ', '.join(params['bcc'])
        if params['subject_prefix'] not in [None, '']:
            subject = '%s %s' % (params['subject_prefix'],
                                 params['subject'])
        else:
            subject = params['subject']
        msg['Subject'] = Header(subject)

        part = MIMEText(body)
        msg.attach(part)
        server.send_message(msg)


def load(app):
    app.handler.register(SMTPMailHandler)
