'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# URIRef
Module | `uriref.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''

__all__ = ['URIRef']

from logging import getLogger

from .identifier import Identifier


class URIRef(Identifier):
    _invalid_chars = '<>" {}|\\^`'

    __slots__ = ()

    @staticmethod
    def is_valid(self):
        return all(map(lambda c: ord(c) > 256 or not c in URIRef._invalid_chars, self))

    def toPython(self):
        return str(self)

    def __add__(self, other):
        return self.__class__(str(self) + other)

    def __getnewargs__(self):
        return (str(self))

    def __mod__(self, other):
        return self.__class__(str(self) % other)

    def __new__(cls, value):
        if not URIRef.is_valid(value):
            getLogger(__name__).warning('%s does not look like a valid URI, trying to serialize this will break.' % value)
        return str.__new__(cls, value)

    def __radd__(self, other):
        return self.__class__(other + str(self))

    def __reduce__(self):
        return (URIRef, (str(self)))

    def __repr__(self):
        return "URIRef('%s')" % str(self)
