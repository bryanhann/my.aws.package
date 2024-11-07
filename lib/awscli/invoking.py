#!/usr/bin/env python3

import json

from util import ezrun, note, bold

from .wrapping import WRAPPER


class Profile:
    def __repr__(s):
        return f"<Profile: {s._profile}>"
    def __init__(self,profile):
        self._profile = profile
    def invoke( self, line, args='' ):
        if not args:
            cmd=line.split()[0]
            args = line[len(cmd):].strip()
        else:
            cmd=line
        wrapper = WRAPPER(cmd.replace('-','_'))
        cmdline = f"aws ec2 --profile {self._profile} {cmd.replace('_','-')} {args}"
        it = ezrun(cmdline)
        return Meta(it, cmdline, wrapper)

class Meta:
    def __repr__(s):
        it=s._it
        out=s.stdout[:1000] + 'df'
        err=s.stderr.rstrip()
        if err: err=f"\n\n---- stderr {'-'*50}\n{err}"
        if out: out=f"\n\n---- stdout {'-'*50}\n{out}"
        return bold(f"""==== <Meta> {'='*60}
    exec: [{s._line}]
    code: [{it.returncode}]
    wrapper: {s._wrapper.__name__}
    wrap: {s._wrap} {err} {out}\n{'='*50}
    """)
    def __bool__(self):
        return bool(self._wrap is not None)
    def __init__(self, it, cmdline, wrapper=None):
        self._it = it
        self._line = cmdline
        self._wrapper = wrapper
        self._wrap = None
        if wrapper:
            try: self._wrap = wrapper(json.loads(self._it.stdout))
            except: pass
        self.stdout = self._it.stdout.decode('utf-8')
        self.stderr = self._it.stderr.decode('utf-8')
    def wrapped(self):
        return self._wrap


def wrap4profile4name(profile,name,args=''):
    return meta4profilername(profile,name,args='').wrapped()
def meta4profile4name(profile,name,args=''):
    wrapper = WRAPPER(name.replace('-','_'))
    it  = invoke4profile4name(profile,name,args)
    return Meta(it, wrapper)

def invoke4profile4name(profile,name,args=''):
    cmdline = f"aws ec2 --profile {profile} {name.replace('_','-')} {args}"
    it = ezrun(cmdline, show=True)
    return it
    out = it.stdout or {'STATE':'Error'}
    return json.loads(out), it

class INVOKER:
    def __init__(self, profile):
        self.profile = profile
    def __getattr__(self, name):
        def fn(profile, name=name):
            return WRAPPER(name)(invoke4profile4name(profile,name))
        return fn(self.profile)

