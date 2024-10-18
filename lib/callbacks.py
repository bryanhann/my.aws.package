#!/usr/bin/env python3

def opt(*args,**kwargs):
    def inner(ctx,option,value):
        ctx.obj.opts[ option.name ] = value
    return inner

def meta(*args,**kwargs):
    def inner(ctx,option,value):
        name = option.name
        if name.startswith( 'x_' ):
            name=name[2:]
        setattr(ctx.obj.meta, name, value)
    return inner

def post(*args,**kwargs):
    def inner(ctx,option,value):
        name = option.name
        if name.startswith( 'x_' ):
            name=name[2:]
        setattr(ctx.obj.post, name, value)
    return inner

def flag(*args,**kwargs):
    def inner(ctx,option,value):
        if value:
            ctx.obj.opts[ option.name ] = ''
    return inner

