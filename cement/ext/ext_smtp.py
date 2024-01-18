"""
Cement smtp extension module.
"""

import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
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

        # allow files to append
        params['files'] = kw.get('files', [])

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

        else:
            server = smtplib.SMTP(params['host'], params['port'],
                                  params['timeout'])
            LOG.debug("%s : initiating smtp" % self._meta.label)

        if self.app.debug is True:
            server.set_debuglevel(9)

        if is_true(params['tls']):
            LOG.debug("%s : initiating tls" % self._meta.label)
            server.starttls()

        if is_true(params['auth']):
            server.login(params['username'], params['password'])

        self._send_message(server, body, **params)
        server.quit()

    def _send_message(self, server, body, **params):
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf-8')

        msg['From'] = params['from_addr']
        msg['To'] = ', '.join(params['to'])
        if params['cc']:
            msg['Cc'] = ', '.join(params['cc'])
        if params['bcc']:
            msg['Bcc'] = ', '.join(params['bcc'])
        if params['subject_prefix'] not in [None, '']:
            subject = '%s %s' % (params['subject_prefix'],
                                 params['subject'])
        else:
            subject = params['subject']
        msg['Subject'] = Header(subject)
        # add body as text and or or as html
        partText = None
        partHtml = None
        if isinstance(body, str):
            partText = MIMEText(body)
        elif isinstance(body, list):
            if len(body) >= 1:
                partText = MIMEText(body[0])
            if len(body) >= 2:
                partHtml = MIMEText(body[1], 'html')
        elif isinstance(body, dict):
            if 'text' in body:
                partText = MIMEText(body['text'])
            if 'html' in body:
                partHtml = MIMEText(body['html'], 'html')
        if partText:
            msg.attach(partText)
        if partHtml:
            msg.attach(partHtml)
        # loop files
        for path in params['files']:
            part = MIMEBase('application', 'octet-stream')
            # test filename for a seperate attachement disposition name (filename.ext=attname.ext)
            filename = os.path.basename(path)
            # test for divider in filename
            i = filename.find('=')
            # split attname from filename
            if i < 0:
                attname = filename
            else:
                attname = filename[i + 1 :]
                filename = filename[0:i]
                # update the filename to read from
                path = os.path.dirname(path) + '/' + filename
            # add attachment
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            # encode and name
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attname}')
            msg.attach(part)

        server.send_message(msg)


def load(app):
    app.handler.register(SMTPMailHandler)
