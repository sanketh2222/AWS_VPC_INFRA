from aws_cdk import core
from aws_cdk import aws_s3
from aws_cdk import aws_ec2
from aws_cdk import aws_kms as _kms

class NewStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,is_prod=False, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        
        print(self.node.try_get_context('prod')['kms_arn'])
        
        kms_key=_kms.Key.from_key_arn(
            self,
            "mykeyid",
            self.node.try_get_context('prod')['kms_arn']
        )
        
    
        print(kms_key)
       g
        
        if is_prod:
            artifact=aws_s3.Bucket(
                self,
                "Myprodbuck",
                 block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
                 encryption=aws_s3.BucketEncryption.KMS,
                 encryption_key=kms_key,
                 removal_policy=core.RemovalPolicy.RETAIN
            )
        else:
            aws_s3.Bucket
            (
                 self,
                "pdid"
             )

            

