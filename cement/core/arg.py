"""
Cement core argument module.

"""

from abc import abstractmethod
from ..core.handler import Handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class ArgumentHandlerBase(Handler):

    """
    This class defines the Argument Handler Interface.  Classes that
    implement this interface must provide the methods and attributes defined
    below.

    Example:

    .. code-block:: python

        from cement.core.arg import ArgumentHandlerBase

        class MyArgumentHandler(ArgumentHandlerBase):
            class Meta:
                label = 'my_argument_handler'

    """
    class Meta:

        """Interface meta-data options."""

        #: The string identifier of the interface.
        interface = 'argument'

    @abstractmethod
    def add_argument(self, *args, **kw):
        """Add arguments to the parser.

        This should be ``-o/--option`` or positional. Note that the interface
        defines the following parameters so that at the very least, external
        extensions can guarantee that they can properly add command line
        arguments when necessary.  The implementation itself should, and will
        provide and support many more options than those listed here.  That
        said, the implementation must support the following:

        Args:
            args (list): List of option arguments.  Generally something like
                ``['-h', '--help']``.

        Keyword Args:
            dest (str): The destination name (variable).  Default: `args[0]`
            help (str): The help text for ``--help`` output (for that argument).
            action (str): Must support: ``['store', 'store_true', 'store_false',
                'store_const']``
            choices (list): A list of valid values that can be passed to an
                option whose action is ``store``.
            const (str): The value stored if ``action == 'store_const'``.
            default (str): The default value.

        Returns:
            None

        """
        pass    # pragma: nocover

    @abstractmethod
    def parse(self, *args):
        """
        Parse the argument list (i.e. ``sys.argv``).  Can return any object as
        long as its' members contain those of the added arguments.  For
        example, if adding a ``-v/--version`` option that stores to the dest of
        ``version``, then the member must be callable as ``Object().version``.

        Args:
            args (list): A list of command line arguments

        Returns:
            object: A callable object whose member reprisent the available
            arguments

        """
        pass    # pragma: nocover


class ArgumentHandler(ArgumentHandlerBase):

    """Argument handler implementation"""

    pass    # pragma: nocover
