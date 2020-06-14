#!/usr/bin/env python3

from aws_cdk import core

#from new.new_stack import NewStack

from resource_stack.customvpc_stack import Customvpc

from resource_stack.MyEc2Stack import MyEc2Stack












app = core.App()

print(app.node.try_get_context('envs')['prod']['mail'])

core.Tag.add(app,key="OwnerMail",value=app.node.try_get_context('envs')['prod']['mail'])

env_US=core.Environment(account=app.node.try_get_context('envs')['prod']['account'],
                        region=app.node.try_get_context('envs')['prod']['region'])
#env_Europe=core.Environment(account=app.node.try_get_context('dev')['account'],region=app.node.try_get_context('dev')['region'])

#print(app.node.try_get_context('dev')['region'])

#print(app.node.try_get_context('@aws-cdk/core:enableStackNameDuplicates'))

#VPC Stack
# Customvpc(app, "myvpcstack",env=env_US)  


#EC2 Stack
MyEc2Stack(app,"MyEc2Stack",env=env_US)




#NewStack(app, "mydevstack1",env=env_US)

#NewStack(app,"myprodstack1",is_prod=True,env=env_US)

app.synth()
