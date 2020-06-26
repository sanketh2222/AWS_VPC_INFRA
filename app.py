#!/usr/bin/env python3

from aws_cdk import core


#from new.new_stack import NewStack

#from resource_stack.customvpc_stack import Customvpc
from app_db_stack.appStack import  MyEc2AsgStack

#from resource_stack.MyEc2Stack import MyEc2Stack

#from  resource_stack.MyEc2AsgStack import MyEc2AsgStack
from  app_db_stack.Vpcstack import  Customvpc

from app_db_stack.appDBStack import RdsStack

from cfn_stacks.CfnPreImfort import CfnStack
from   resource_stack.SecretStack import  MySecretStack

from resource_stack.iamStack import  MyIAMStack

from resource_stack.resourcePolicies import ResourceStack

from resource_stack.CustomS3ResPolicy import S3CustomResourceStack

from cfn_stacks.snssubStack import SnsSubStack






app = core.App()


SnsSubStack(app,"SnsSubStack")
#print(app.node.try_get_context('envs')['prod']['ohio'])

core.Tag.add(app,key="OwnerMail",value=app.node.try_get_context('envs')['prod']['mail'])

env_US=core.Environment(account=app.node.try_get_context('envs')['prod']['account'],
                        region=app.node.try_get_context('envs')['prod']['region'])

env_oh=core.Environment(account=app.node.try_get_context('envs')['prod']['account'],
                        region=app.node.try_get_context('envs')['prod']['ohio'])
#env_Europe=core.Environment(account=app.node.try_get_context('dev')['account'],region=app.node.try_get_context('dev')['region'])

#print(app.node.try_get_context('dev')['region'])

#print(app.node.try_get_context('@aws_cdk/core:enableStackNameDuplicates'))

#VPC Stack
 
#vpcstack=Customvpc(app,"myvpcstack")  

 
CfnStack(app,"CfnStack")

#EC2 Stack 1
#MyEc2Stack(app,"MyEc2Stack",env=env_US) 



#EC2 Stack2
#MyEc2Stack(app,"MyOhioStack",env=env_oh)



#autoscalling stacks
#ec2stack=MyEc2AsgStack(app,"MyASGStack",vpcstack.vpc)


#rds stack
#RdsStack(app,"RDSStack",vpc=vpcstack.vpc,securitygroups=ec2stack.web_Server_asg.connections.security_groups)


#secrets and ssm
MySecretStack(app,"SecreteStack")


#IAM Stack
#MyIAMStack(app,"IAMStack")


#Resource Stack
#ResourceStack(app,"ResStack")

# S3 Resource stack
#S3CustomResourceStack(app,"S3ResStack")

#NewStack(app, "mydevstack1",env=env_US)


#NewStack(app,"myprodstack1",is_prod=True,env=env_US)

app.synth()
