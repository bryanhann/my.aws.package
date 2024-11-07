#!/usr/bin/env python3
import click

import config
import myclick.callbacks as CB


@click.group()
@click.pass_context
@click.option(
    '--x-show'
    , callback=CB.meta()
    , is_flag=True
    , default=True
    , help='disable showing the aws command line'
)
@click.option(
    '--x-dry'
    , callback=CB.meta()
    , is_flag=True
    , default=False
    , help='just show the aws command (do not execute)'
)
@click.option(
    '--profile'
    , callback=CB.opt()
    , default=config.PROFILE
    , help="aws profile override"
)
@click.option(
    '--dry-run'
    , callback=CB.flag()
    , is_flag=True
    , flag_value=True
)

def keys(ctx,**opts):
    """Handle aws keypairs
    Option that start --x- are not passed to aws
    """
    pass


