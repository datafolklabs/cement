"""Cement core meta functionality."""

import inspect

class Meta(object):

    """
    Model that acts as a container class for a meta attributes for a larger
    class. It stuffs any kwarg it gets in it's init as an attribute of itself.

    """

    def __init__(self, **kwargs):
        self._merge(kwargs)

    def _merge(self, dict_obj):
        for key in dict_obj.keys():
            setattr(self, key, dict_obj[key])


class MetaMixin(object):

    """
    Mixin that provides the Meta class support to add settings to instances
    of objects. Meta settings cannot start with a _.

    """

    def __init__(self, *args, **kwargs):
        # Get a List of all the Classes we in our MRO, find any attribute named
        #     Meta on them, and then merge them together in order of MRO
        # metas = reversed([x.Meta for x in self.__class__.mro()
        #                   if hasattr(x, "Meta")])

        final_meta = {}

        # Merge the Meta classes into one dict
        # for meta in metas:
        #     final_meta.update(dict([x for x in meta.__dict__.items()
        #                             if not x[0].startswith("_")]))

        print('_' * 30)
        # new class-variable based meta
        for mro in reversed(self.__class__.mro()):
            print(mro)
            class_metas = {key:value for key, value in mro.__dict__.items() 
                           if not key.startswith('_') 
                              and not inspect.isfunction(value)
                              and not isinstance(value, property)}
            print(class_metas)
            final_meta.update(class_metas)

        # Update the final Meta with any kwargs passed in
        for key,val in final_meta.items():
            if key in kwargs:
                final_meta[key] = kwargs.pop(key)
            setattr(self, key, val)

        self._meta = Meta(**final_meta)


        # FIX ME: object.__init__() doesn't take params without exception
        super(MetaMixin, self).__init__()
