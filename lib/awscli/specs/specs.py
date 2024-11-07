#!/usr/bin/env python3


from dataclasses import dataclass

IMAGE_ID_SUSE    = "ami-0226a08ab7f8c5d03"
IMAGE_ID_UBUNTU  = "ami-048ddca51ab3229ab"

def fix(key): return key.replace('_','-')

@dataclass
class Spec_ABC:
    def base(self):
        return [f"--{fix(k)} {v}" for k,v in self.__dict__.items() ]

    def tag(self,**d):
        def tag4pair(pair): return "{Key=%s,Value=%s}" % pair
        aa = ','.join(map(tag4pair,d.items()))
        val = f"ResourceType=instance,Tags=[{aa}]"
        return [ f"--tag-specifications  {val}" ]
    def cmd4name(self, name):
        acc = [ f"--key-name {name}" ]
        acc += self.base()
        acc += self.tag(Name=name,zappa='frank',spec=self.__class__.__name__  )
        return ' '.join(acc)

@dataclass
class Ubuntu(Spec_ABC):
    security_group_ids: str = "sg-0b9a4ef40ee78a621"
    image_id:           str = IMAGE_ID_UBUNTU
    count:              str =  "1"
    instance_type:      str = "t2.micro"
    subnet_id:          str = "subnet-051fcbe4e4f4cc521"

@dataclass
class Suse(Spec_ABC):
    security_group_ids: str = "sg-0b9a4ef40ee78a621"
    image_id:           str = IMAGE_ID_SUSE
    count:              str =  "1"
    instance_type:      str = "t2.micro"
    subnet_id:          str = "subnet-051fcbe4e4f4cc521"

