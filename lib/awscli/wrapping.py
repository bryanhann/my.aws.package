#!/usr/bin/env python3

from importlib import import_module
from util import abort, note, stdout, note
from importlib import import_module
def warn(txt):
    stdout( f'warning: {txt}' )

class Wrap():
    def __init__(self,dikt={}):
        self._dikt = dikt
    def __getitem__(self, key):
        return self._dikt[key]
    def __repr__(self):
        return f"<{self.__class__.__name__}>"
    def keys(self):
        return self._dikt.keys()
    def items(self):
        return self._dikt.items()
    def values(self):
        return self._dikt.values()

    def __getattr__(self, name):
        try:
            val = self._dikt[name]
        except KeyError:
            raise KeyError( f"class {self.__class__.__name__} cannot resolve [{name}]" )
        return val
        module = import_module(self.__class__.__module__)
        try:                    wrap = getattr(module, name)
        except AttributeError:  wrap = None


        #if wrap: return wrap(val)
        return val


class Wrapper:
    def __call__(self,name):
        return getattr(self,name)
    def __getattr__(self, name):
        dotted = f"{__package__}.aws.ec2.{name}"
        path = dotted.replace('.','/') + '.py'
        try:
            return import_module(dotted).ROOT
            return import_module(f"{__package__}.aws.ec2.{name}").ROOT
        except ModuleNotFoundError:
            warn(f'Wrapper: cannot find [{path}].')
        except AttributeError:
            warn(f'Wrapper: cannot load [{path}].')
        from awscli.aws.ec2.DUMMY import DUMMY
        return DUMMY
WRAPPER = Wrapper()

