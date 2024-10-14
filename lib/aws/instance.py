#!/usr/bin/env python3

class Instance:
    def __init__(self, root):
        self._root = dict(root)
    def __getattr__(self, name):
        try:
            return self._root[name]
        except KeyError:
            return None
    def id(self):
        return self.InstanceId
    def tags(self):
        return dict( (tag['Key'], tag['Value']) for tag in self.Tags )
    def name(self):
        return self.tags()['Name']
    def state(self):
        return self.State['Name']
    def ip(self):
        try:
            return self.PublicIpAddress
        except AttributeError:
            return ""
    def __repr__(self):
        acc = []
        acc.append(self.name()+':')
        acc.append( self.state() )
        if self.ip():
            acc.append( self.ip() )
        return '<' + ' '.join(acc) + '>'

