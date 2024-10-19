#!/usr/bin/env python3
import sys
import subprocess

from util import bold as BOLD
from util import stderr as ERR
from util import stdout as OUT


class Wrap:
    def __init__(self, it, parent, *a,**b):
        self.stdout =  it.stdout.decode('utf-8')
        self.stderr =  it.stderr.decode('utf-8')
        self.returncode = it.returncode
        self.parent = parent
        ('die' in b) and self.error_and_die()
    def normal(self):
        meta = self.parent.meta
        if not hasattr(meta,'out'): meta.out=True
        if not hasattr(meta,'err'): meta.err=True
        self.parent.meta.out and OUT(self.stdout)
        self.parent.meta.err and ERR(self.stderr)
    def error_and_die(self):
        if self.returncode != 0:
            ERR(self.stderr)
            exit('error_and_die')

class Command_Runner:
    @property
    def x(self):
        class obj4dict:
            def __init__(self, d={} ): self.__dict = d
            def __getattr__(self, name):
                try: return f'--{name} {self.__dict[name]}'
                except KeyError: return ''
        return obj4dict(self.opts)

    def __init__(self, cmd ):
        class Namespace: pass
        self._cmd = cmd
        self.opts = {}
        self.xopts = {}
        self.meta = Namespace()
        self.post = Namespace()

    def __call__(self, cmd, *a, **b):
        it = self.run(cmd)
        return Wrap(it, parent=self, *a, **b)

    def add_option(self,name,val):
        self.opts[name.replace('-','_')] = val

    def run(self, cmd, show=True, dry=False):
        opts = ' '.join([ f"--{key.replace('_','-')} {val}" for key,val in self.opts.items() ])
        line = f"{self._cmd} {cmd} {opts}"
        showline=line.replace('--','\n    --')
        (show and self.meta.show) and ERR(BOLD(showline))
        (dry or self.meta.dry)    and exit('end dry run')
        it = subprocess.run(line.split(), capture_output=True)
        return it
