"""Cement core cache module."""

from abc import abstractmethod
from ..core.handler import Handler
from ..utils.misc import minimal_logger

LOG = minimal_logger(__name__)


class CacheHandlerBase(Handler):

    """
    This class defines the Cache Handler Interface.  Classes that
    implement this interface must provide the methods and attributes defined
    below.

    Usage:

    .. code-block:: python

        from cement.core.cache import CacheHandlerBase

        class MyCacheHandler(CacheHandlerBase):
            class Meta:
                label = 'my_cache_handler'
            ...

    """

    #: The string identifier of the interface.
    interface = 'cache'

    @abstractmethod
    def get(self, key, fallback=None):
        """
        Get the value for a key in the cache.  If the key does not exist
        or the key/value in cache is expired, this functions must return
        'fallback' (which in turn must default to None).

        :param key: The key of the value stored in cache
        :param fallback: Optional value that is returned if the cache is
         expired or the key does not exist.  Default: None
        :returns: Unknown (whatever the value is in cache, or the `fallback`)

        """
        pass

    @abstractmethod
    def set(self, key, value, time=None):
        """
        Set the key/value in the cache for a set amount of `time`.

        :param key: The key of the value to store in cache.
        :param value: The value of that key to store in cache.
        :param time: A one-off expire time.  If no time is given, then a
            default value is used (determined by the implementation).
        :type time: ``int`` (seconds) or ``None``
        :returns: ``None``

        """
        pass

    @abstractmethod
    def delete(self, key):
        """
        Deletes a key/value from the cache.

        :param key: The key in the cache to delete.
        :returns: True if the key is successfully deleted, False otherwise.
        :rtype: ``boolean``

        """
        pass

    @abstractmethod
    def purge():
        """
        Clears all data from the cache.

        """
        pass


class CacheHandler(CacheHandlerBase):

    """
    Cache handler implementation.

    """
    pass
