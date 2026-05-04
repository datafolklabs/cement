"""Cement core meta functionality."""

from typing import Any


class Meta:

    """
    Container class for meta attributes of a larger class. Keyword arguments
    are set as attributes of ``self``.

    """

    # D-09: Meta classes carry user-arbitrary attributes by design
    # (config_defaults, extensions, handlers, hooks, ...). The wide kwargs
    # type IS the public Meta contract (D-12). `_merge` is internal but the
    # dict it merges has the same arbitrary-value contract.
    def __init__(self, **kwargs: Any) -> None:
        self._merge(kwargs)

    # D-09: same arbitrary-value contract as `__init__` above.
    def _merge(self, dict_obj: dict[str, Any]) -> None:
        for key in dict_obj.keys():
            setattr(self, key, dict_obj[key])


class MetaMixin:

    """
    Mixin that provides the meta class support to add settings to instances
    of objects. Meta keys cannot start with a ``_``.

    """

    # D-09: same Meta arbitrary-attribute contract — `*args` accepts any
    # positional cooperative-multi-inheritance super() chain payload.
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Get a List of all the Classes we in our MRO, find any attribute named
        #     Meta on them, and then merge them together in order of MRO
        metas = reversed([x.Meta for x in self.__class__.mro()
                          if hasattr(x, "Meta")])
        final_meta = {}

        # Merge the Meta classes into one dict
        for meta in metas:
            final_meta.update(dict([x for x in meta.__dict__.items()
                                    if not x[0].startswith("_")]))

        # Update the final Meta with any kwargs passed in
        for key in final_meta.keys():
            if key in kwargs:
                final_meta[key] = kwargs.pop(key)

        self._meta = Meta(**final_meta)

        # FIX ME: object.__init__() doesn't take params without exception
        super().__init__()
