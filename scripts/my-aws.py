#!/usr/bin/env python3
import sys
from pathlib import Path

import click

lib = Path(__file__).parent.parent/'lib'
sys.path.append(str(lib))

from aws import allinstances, inst4name, ip4name
from aws.util import stderr, cli, run

PROFILE='showme'
REFRESH=True

@click.group()
@click.option('--cache/--no-cache', type=bool, default=False, help='Use cached')
def group(cache):
    """
    Control ec2 instances.
    First argument must be the name as per tag.
    """
    allinstances(refresh=True)
    #if not cache:
    #    print( 'REFRESHING CACNE')
    #    allinstances(refresh=True)



#----------------------------------------------------------
# list

@click.command()
def list():
    """list all aws ec2 instances with state

    They must have tag naming them.
    """
    for inst in allinstances():
        print(inst)


#----------------------------------------------------------
# start <name>

@click.command()
@click.option('--profile', default=PROFILE)
@click.option('--cli', 'method', flag_value='cli', default=True)
@click.option('--run', 'method', flag_value='run')
@click.argument('name')
def start(name,method,profile):
    inst=inst4name(name)
    if not inst: return
    line = f"aws ec2 --profile {profile} start-instances --instance-ids {inst.id()}"
    if method=='cli': cli(line)
    else: run(line)


#----------------------------------------------------------
# stop <name>

@click.command()
@click.argument('name')
def ip(name):
    """Echo the public ip address of ec2 instance to STDOUT"""
    print( ip4name(name))
    return
    inst=inst4name(name)
    if not inst: return
    if not inst.ip():
        return
    print(inst.ip())

@click.command()
@click.option('--profile', default=PROFILE)
@click.argument('name')
@click.option('--cli', 'method', flag_value='cli', default=True)
@click.option('--run', 'method', flag_value='run')
def stop(name,method, profile):
    inst=inst4name(name)
    if not inst: return
    line = f"aws ec2 --profile {profile} stop-instances --instance-ids {inst.id()}"
    if method=='cli': cli(line)
    else: run(line)

#----------------------------------------------------------
# ssh <name>

@click.command()
@click.option('--user', default='ubuntu')
@click.option('--profile', default=PROFILE)
@click.option('--cli', 'method', flag_value='cli', default=True)
@click.option('--run', 'method', flag_value='run')
@click.argument('name')
def ssh(name,method,profile,user):
    host=ip4name(name)
    if not host:
        print( 'host is not running' )
        return
    pem=f"~/.ssh/{name}.pem"
    line= f"ssh -i {pem} {user}@{host}"
    if method=='cli': cli(line)
    else: run(line)

group.add_command(ssh)
group.add_command(ip)
group.add_command(start)
group.add_command(stop)
group.add_command(list)

if __name__ == '__main__':
    group()

