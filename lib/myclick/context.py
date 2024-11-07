#!/usr/bin/env python3

from util import note, abort
from awscli.invoking import Profile


class Context:
    def __call__(self, line, loud=False, show=False, die=False, **b):
        show and note( f">>> {self.__class__.__name__}({line})" )
        meta = self.Profile.invoke( line )
        meta and loud and note(repr(meta))
        not meta and die and abort('CTX aborting')
        return meta
    def __init__(self, ctx):
        self.Profile = Profile(ctx.obj.opts['profile'])

class KEYS(Context):
    def delete(self,name):
        note( f'deleting keypair [{name}]...' )
        wrap = self(f'delete-key-pair --key-name {name}', loud=False, show=True)._wrap
        note( f'keypair [{name}] is now deleted.' )
    def names(s):
        wrap = s( "describe-key-pairs", die=True)._wrap
        return [x.name() for x in wrap.keypairs()]


