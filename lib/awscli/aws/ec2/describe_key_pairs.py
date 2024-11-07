#!/usr/bin/env python3
from awscli import Wrap

class DESCRIBE_KEY_PAIRS(Wrap):
    def keypairs(self):
        return [ KeyPair(x) for x in self.KeyPairs ]

class KeyPair(Wrap):
    def name(self):
        return self.KeyName
    def __repr__(self):
        return( f'<{self.__class__.__name__} {self.KeyName}' )

ROOT=DESCRIBE_KEY_PAIRS
