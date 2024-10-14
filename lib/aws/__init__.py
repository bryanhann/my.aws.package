#!/usr/bin/env python3
import json
import subprocess
import aws.instance
import pathlib
import sys
from aws.util import stderr
from aws.util import bold
from aws.instance import Instance
TMP=pathlib.Path.home()/'tmp'
TMP.is_dir() or TMP.mkdir()
SRC=TMP/'tmp.aws.output'


def _load():
    try:
        sys._MAGIC_LOADED
        return
    except AttributeError:
        pass
    sys._MAGIC_LOADED=True
    print('allinstances is refreshing')
    if SRC.exists():
        SRC.unlink()
    with open(SRC, 'w') as fd:
        print('RUNNING IN BACKGROUND:')
        line = 'aws ec2 describe-instances --profile showme'
        print( f'    {bold(line)}' )
        subprocess.run( 'aws ec2 describe-instances --profile showme'.split(), stdout=fd )


def allinstances(refresh=False):
    _load()
    _load()
    #try:
    #    sys._MAGIC_LOADED
    #except AttributeError:
    #    sys._MAGIC_LOADED=True
    #    print('allinstances is refreshing')
    #    if SRC.exists():
    #        SRC.unlink()
    #    with open(SRC, 'w') as fd:
    #        subprocess.run( 'aws ec2 describe-instances --profile showme'.split(), stdout=fd )

    with open(SRC) as fd:
        ACC=[]
        for res in json.load(fd)['Reservations']:
            for instance in res['Instances']:
                 #yield Instance(instance)
                 ACC.append(Instance(instance))
        for x in ACC:
            yield(x)
        #return ACC


def inst4name(name):
    acc = [inst for inst in allinstances() if inst.name() == name]
    if len(acc)==0:
        stderr(f'No machine name [{name}]')
        return None
    if len(acc)==1:
        return acc[0]
    raise Exception('too many')

def allnames():
    return [x.name() for x in allinstanced()]

def id4name(name):
    return inst4name(name).id()

def ip4name(name):
    inst=inst4name(name)
    return (inst and inst.ip()) or ''

