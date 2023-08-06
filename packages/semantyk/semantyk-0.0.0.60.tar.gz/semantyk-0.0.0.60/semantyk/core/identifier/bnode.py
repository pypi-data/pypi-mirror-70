'''
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# BNode
Module | `bnode.py`

Daniel Bakas Amuchastegui\
May 21, 2020

Copyright © Semantyk 2020. All rights reserved.\
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
'''

__all__ = ['BNode']

from ...uuid_generator import generate_uuid
from .identifier import Identifier


class BNode(Identifier):
    __slots__ = ()

    def toPython(self):
        return str(self)

    def __getnewargs__(self):
        return (str(self))

    def __new__(cls, value=None):
        return Identifier.__new__(cls, value or generate_uuid())

    def __reduce__(self):
        return (BNode, (str(self)))

    def __repr__(self):
        return "BNode('%s')" % self