from aws_cdk import core
from aws_cdk import aws_dynamodb as _d
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_apigateway as _apig
from aws_cdk import aws_logs as _logs


import json
import os


class ApiGatewayStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        try:
            with open("serverless_stack/hello.py",mode="r") as f:
                lambda_code=f.read()
                print("file read\n")
        except OSError:
            print("file not found")
            
        #lambda function with inline code stored in local
        log_fn=_lambda.Function(
            self,
            "lambdafn",
            # code=_lambda.InlineCode(lambda_code),
            code=_lambda.Code.from_inline(lambda_code),
            handler="index.lambda_handler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            environment={
                "var":"1",# not able to set integer values 
                "LOG_LEVEL": "INFO"# CREATES ENVIRONMENT VARIABLES
            },
            reserved_concurrent_executions=1,
            timeout=core.Duration.seconds(3),
            function_name="apicode"
        )
        
        
        log_grps=_logs.LogGroup(
            self,
            "lggrps",
            log_group_name=f"/aws/lambda/{log_fn.function_name}",
            removal_policy=core.RemovalPolicy.DESTROY,
            retention=_logs.RetentionDays.FIVE_DAYS
        )
        
        
        print(f" return type is   {log_fn}")
        
        # creating the api gateway
        api_gwy=_apig.LambdaRestApi(
            self,
            "apigwy",
            handler=log_fn
            
        )
        
        output=core.CfnOutput(
           self,
           "url",
           description="api gateway url",
           value=api_gwy.url
        )