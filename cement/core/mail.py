"""Cement core mail module."""

from ..core import interface, handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


def mail_validator(klass, obj):
    """Validates a handler implementation against the IMail interface."""

    members = [
        '_setup',
        'send',
    ]

    ### FIX ME: Validate Configuration Defaults Here

    interface.validate(IMail, obj, members)


class IMail(interface.Interface):
    """
    This class defines the Mail Handler Interface.  Classes that
    implement this handler must provide the methods and attributes defined
    below.

    Implementations do *not* subclass from interfaces.

    Usage:

    .. code-block:: python

        from cement.core import mail

        class MyMailHandler(object):
            class Meta:
                interface = mail.IMail
                label = 'my_mail_handler'
            ...

    """
    # pylint: disable=W0232, C0111, R0903
    class IMeta:

        """Interface meta-data."""

        label = 'mail'
        """The label (or type identifier) of the interface."""

        validator = mail_validator
        """Interface validator function."""

    # Must be provided by the implementation
    Meta = interface.Attribute('Handler meta-data')

    def _setup(app_obj):
        """
        The _setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.

        :param app_obj: The application object.
        :returns: None

        """

    def send(body, **kwargs):
        """
        Send a mail message.  Keyword arguments override defaults defined
        in the handler implementations configuration (see possible keyword
        arguments below).

        :param body: The message body to send
        :type body: Multiline string
        :keyword to: List of recipients (generally email addresses)
        :keyword cc: List of CC Recipients
        :keyword bcc: List of BCC Recipients
        :keyword from: Address (generall email) of the sender
        :keyword subject: Message subject line
        :returns: Boolean (``True`` if message is sent successfully, ``False``
         otherwise)

        """


class CementMailHandler(handler.CementBaseHandler):
    """
    Base class that all Mail Handlers should sub-class from.

    """
    class Meta:
        """
        Handler meta-data (can be passed as keyword arguments to the parent
        class).
        """

        #: String identifier of this handler implementation.
        label = None

        #: The interface that this handler class implements.
        interface = IMail

        #: Configuration default values
        config_defaults = {
            'to' : [],
            'from' : 'noreply@example.com',
            'cc' : [],
            'bcc' : [],
            'subject' : 'Default Subject Line',
            'subject_prefix' : '',
            }

    def __init__(self, *args, **kw):
        super(CementMailHandler, self).__init__(*args, **kw)

    def _setup(self, app_obj):
        super(CementMailHandler, self)._setup(app_obj)
        self._validate_config()

    def send(self, body, **kw):
        raise NotImplementedError

    def _validate_config(self):
        # convert comma separated strings to lists (ConfigParser)
        for item in ['to', 'cc', 'bcc']:
            if item in self.app.config.keys(self._meta.config_section):
                value = self.app.config.get(self._meta.config_section, item)

                # convert a comma-separated string to a list
                if type(value) is str:
                    value_list = value.split(',')

                    # clean up extra space if they had it inbetween commas
                    value_list = (x.strip() for x in value_list)

                    # set the new extensions value in the config
                    self.app.config.set(self._meta.config_section, item,
                                        value_list)


class DummyMailHandler(CementMailHandler):
    class Meta:
        label = 'dummy'

    def _get_params(self, **kw):
        params = dict()
        for item in ['to', 'from', 'cc', 'bcc', 'subject', 'subject_prefix']:
            config_item = self.app.config.get(self._meta.config_section, item)
            params[item] = getattr(kw, item, config_item)

        return params

    def send(self, body, **kw):
        # shorted config values
        params = self._get_params(**kw)
        msg = "\n" + "=" * 77 + "\n"
        msg += "DUMMY MAIL MESSAGE\n"
        msg += "-" * 77 + "\n\n"
        msg += "To: %s\n" % ', '.join(params['to'])
        msg += "From: %s\n" % params['from']
        msg += "CC: %s\n" % ', '.join(params['cc'])
        msg += "BCC: %s\n" % ', '.join(params['bcc'])
        msg += "Subject: %s%s\n\n---\n\n" % (params['subject_prefix'],
                                    params['subject'])
        msg += body + "\n"

        msg += "\n" + "-" * 77 + "\n"

        print msg

class SMTPMailHandler(CementMailHandler):
    class Meta:
        label = 'smtp'

    def send(self, body, **kw):
        pass

