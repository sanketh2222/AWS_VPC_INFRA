from aws_cdk import aws_secretsmanager as  _secretmanager
from aws_cdk import aws_ssm as _ssm
from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_logs as _logs
import pickle
import json
import os


class MyLambdaStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # code begins
        #importing existing bucket
        s3bkt=_s3.Bucket.from_bucket_name(self,
                                          "mybkt",
                                          bucket_name="mybuck2809")
        try:
            with open("serverless_stack/lambda.py",mode="r") as f:
                lambda_code=f.read()
                print("file read\n")
        except OSError:
            print("file not found")
            
       #lambda function with inline code stored in local
       
           # log_fn=_lambda.Function(
        #     self,
        #     "lambdafn",
        #     # code=_lambda.InlineCode(lambda_code),
        #     code=_lambda.Code.from_inline(lambda_code),
        #     handler="index.lambda_handler",
        #     runtime=_lambda.Runtime.PYTHON_3_7,
        #     environment={
        #         "var":"1",# not able to set integer values
        #         "LOG_LEVEL": "INFO"# CREATES ENVIRONMENT VARIABLES
        #     },
        #     reserved_concurrent_executions=1,
        #     timeout=core.Duration.seconds(3),
        #     function_name="logging_function"
        # )
        
        
        # lambda function with code stored in s3 as a zip file
        log_fn=_lambda.Function(
            self,
            "lfnction",
            code=_lambda.Code.bucket(
                bucket=s3bkt,
                key="lambda.zip"
            ),
            handler="index.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            environment={
                    "var":"1",# not able to set integer values
                    "LOG_LEVEL": "INFO"# CREATES ENVIRONMENT VARIABLES
            },
            reserved_concurrent_executions=1,
            timeout=core.Duration.seconds(3),
            function_name="logging_function"
            
        )
        # adding logs function to make logs as a part of stack so that if stack is deleted the 
        #logs also will be deleted
        # # /aws/lambda/function-name
        
        log_grps=_logs.LogGroup(
            self,
            "lggrps",
            log_group_name=f"/aws/lambda/{log_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.FIVE_DAYS
        )
        
        output= core.CfnOutput(
            self,
            "FN-Name",
            description="name of the function",
            value=log_fn.function_name
        )