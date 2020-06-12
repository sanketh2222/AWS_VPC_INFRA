#!/usr/bin/env python3

from aws_cdk import core

#from new.new_stack import NewStack

from resource_stack.customvpc_stack import Customvpc




app = core.App()

#env_US=core.Environment(account=app.node.try_get_context('prod')['account'],region=app.node.try_get_context('prod')['region'])
#env_Europe=core.Environment(account=app.node.try_get_context('dev')['account'],region=app.node.try_get_context('dev')['region'])

#print(app.node.try_get_context('dev')['region'])
#print(app.node.try_get_context('@aws-cdk/core:enableStackNameDuplicates'))
Customvpc(app, "myvpcstack")
#NewStack(app, "mydevstack1",env=env_US)
#NewStack(app,"myprodstack1",is_prod=True,env=env_US)

app.synth()
