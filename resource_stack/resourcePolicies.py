from aws_cdk import aws_secretsmanager as  _secretmanager
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_ssm as _ssm
from aws_cdk import core
import json


class ResourceStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # start coding
        
        pass1=_secretmanager.Secret(
            self,
            "autopass",
            description="auto pass for user 1",
            secret_name="IAM_PASS1"
        )
        
        user1=_iam.User(
            self,
            "user1",
            user_name="user1",
            password=pass1.secret_value
        )
        
        
        grpname=_iam.Group(
            self,
            "group",
            group_name="user_group"
        )
        
        grpname.add_user(user1)
        
        
        # add managed policies
        
        grpname.add_managed_policy(
           _iam.ManagedPolicy.from_aws_managed_policy_name(
               "AmazonS3ReadOnlyAccess"
           )
        )
        
        
        param1=_ssm.StringParameter(
            self,
            "param1",
            description="parameter 1",
            parameter_name="/konstone/keys/fish",
            string_value="1126",
            tier=_ssm.ParameterTier.STANDARD
        )
        
        param2=_ssm.StringParameter(
            self,
            "param2",
            description="Parameter 2",
            parameter_name="/konstone/keys/fish/gold",
            string_value="12996",
            tier=_ssm.ParameterTier.STANDARD
        )
        
        param1.grant_read(grpname)
        
        grpstatement=_iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=[
                "ssm:DescribeParameters"
            ]
        )
        
        grpstatement.sid="describeallparameters"
        
        # add my custom statement to already existing policy
        grpname.add_to_policy(
            grpstatement
             
        )
        
        grpstatement2= _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    resources=["*"],
                    actions=[
                         "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "cloudwatch:Get*"
                    ]
                )
        
        grpstatement2.sid="ListingEc2policy"  
        #create a custom managed policy from scratch
        
        listec2insatnces=_iam.ManagedPolicy(
            self,
            "listec2insatnces",
            description="list ec2 insatnces",
            statements=[grpstatement2]
        )
        
        
        grpname.add_managed_policy(
            listec2insatnces
        )