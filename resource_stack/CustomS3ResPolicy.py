from aws_cdk import aws_iam as _iam
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_secretsmanager
from aws_cdk import aws_rds
from aws_cdk import core



class S3CustomResourceStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # start coding
        
        mybkt=_s3.Bucket(
            self,
            "s3buck",
            versioned=True,
            bucket_name="mybuck2809",
            removal_policy=core.RemovalPolicy.DESTROY
        )
        
        print(mybkt.arn_for_objects("*.html"))
        print(f"{mybkt.bucket_arn}/*.html")
        
        
        print(mybkt.from_bucket_arn(self,"bucket",bucket_arn=f"{mybkt.bucket_arn}"))
        print(mybkt.bucket_arn)
        print(mybkt.from_bucket_name(self,"s3bucket",bucket_name="mybuck2809"))
        
        core.CfnOutput(
            self,
            "bucket1",
            value=f"{mybkt.bucket_arn}",
            description="bucket arn for mybuck2809"
        )
        core.CfnOutput(
            self,
            "bucket2",
            value=f"{mybkt.from_bucket_arn}",
            description="bucket arn for mybuck2809"
        )
        
        
        
        mybkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[f"{mybkt.bucket_arn}/*.html"],
                principals=[_iam.AnyPrincipal()]
            )
        )
        
        mybkt.add_to_resource_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{mybkt.bucket_arn}/*"],
                principals=[_iam.AnyPrincipal()],
                conditions={
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
            )
        )
        
       