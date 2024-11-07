#!/usr/bin/env python3
from awscli import Wrap

class CREATE_KEY_PAIR(Wrap):
    def the_material(self):
        return self['KeyMaterial']

ROOT=CREATE_KEY_PAIR
