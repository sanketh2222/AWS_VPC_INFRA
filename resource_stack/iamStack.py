from aws_cdk import aws_secretsmanager as  _secretmanager
from aws_cdk import aws_iam as _iam
from aws_cdk import core
import json


class MyIAMStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # code begins
        
        # autogenerate a password using secrets manager
        pass1=_secretmanager.Secret(
            self,
            "autopass",
            description="password for user1",
            secret_name="IAM_PASS1"
        )
        
        
        #create IAM user1
        user1=_iam.User(
            self,
            "user1",
            password=pass1.secret_value,
            user_name="user1",
            password_reset_required=True
        )
        
        # create IAM user2
        
        user2=_iam.User(
            self,
            "user2",
            password=core.SecretValue.plain_text(
                "badpass"
            ),
            user_name="user2"
        )
        
        
        #create IAM GROUP 
        grp1=_iam.Group(self,
                   "IAMgroup",
                   group_name="TestUsers"
                )
        
        
        #adding user to group created
        grp1.add_user(user1)
        
        
        #generate a signin url
        sign_rul=core.CfnOutput(
            self,
            "signin",
            description="url to access through console",
            value=f"https://{core.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
        )