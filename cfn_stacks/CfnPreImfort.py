from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_rds as _rds
from aws_cdk import core
import json


class CfnStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # start coding
        
        try:
            with open("cfn_stacks/sample_templates/s3buckettemplate.json") as file:
                cfn_template=json.load(file)
                #print(cfn_template)
        except OSError:
            print("cannot find file")
            
            
        template_resource=core.CfnInclude(self,"s3template",
                                 template=cfn_template)
        
        print(template_resource)
        
        #paramname=core.Fn.get_att("KonstoneAssets",attribute_name="Name")
        paramname1=core.Fn.get_att("KonstoneAssets",attribute_name="Value")
        
        
        print(paramname)
        
        
        bkt_arn=core.Fn.get_att("EncryptedS3Bucket",attribute_name="Arn")
        
        
        print(bkt_arn)
        
        
        core.CfnOutput(
            self,
            "printingarn",
            value=f"{bkt_arn.to_string()}",
            description="imported bucket arn"
        )
        
        core.CfnOutput(
            self,
            "printssmvalue",
            value=f"{paramname1.to_string()}",
            description="imported bucket arn"
        ) 