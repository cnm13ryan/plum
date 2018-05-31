# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import logging

__all__ = ['parametric']
log = logging.getLogger(__name__)


def parametric(Class):
    """A decorator for parametric classes."""
    subclasses = {}

    if not issubclass(Class, object):
        raise RuntimeError('To let {} be a parametric class, it must be a '
                           'new-style class.')

    class ParametricClass(Class):
        def __new__(cls, *ps):
            try:
                hash(ps)
            except TypeError:
                raise TypeError('Type parameters must be hashable.')

            if ps not in subclasses:
                def __new__(cls, *args, **kw_args):
                    return Class.__new__(cls)

                name = Class.__name__ + '{' + ','.join(str(p) for p in ps) + '}'
                subclasses[ps] = type(name,
                                      (ParametricClass,),
                                      {'__new__': __new__})
            return subclasses[ps]

    return ParametricClass