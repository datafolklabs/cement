"""NullOutput Framework Extension"""

from ..core import backend, output, handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class NullOutputHandler(output.CementOutputHandler):

    """
    This class is an internal implementation of the
    :ref:`IOutput <cement.core.output>` interface. It does not take any
    parameters on initialization.

    """
    class Meta:

        """Handler meta-data"""

        interface = output.IOutput
        """The interface this class implements."""

        label = 'null'
        """The string identifier of this handler."""

    def render(self, data_dict, template=None):
        """
        This implementation does not actually render anything to output, but
        rather logs it to the debug facility.

        :param data_dict: The data dictionary to render.
        :param template: The template parameter is not used by this
            implementation at all.
        :returns: None

        """
        LOG.debug("not rendering any output to console")
        LOG.debug("DATA: %s" % data_dict)
        return None


def load():
    """Called by the framework when the extension is 'loaded'."""
    handler.register(NullOutputHandler)
