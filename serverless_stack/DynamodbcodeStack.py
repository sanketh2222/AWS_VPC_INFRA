from aws_cdk import core
from aws_cdk import aws_dynamodb as _d
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_logs as _logs


import json
import os


class DynamodbcodeStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        dyn_table=_d.Table(
            self,
            "demotable",
            table_name="mytable1",
            partition_key=_d.Attribute(
                name="id",
                type=_d.AttributeType.NUMBER
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )
        
        # tab=_d.from_table_arn(
        #     self,
        #     "ddb",
        #     table_arn="arn:aws:dynamodb:us-east-1:325764798866:table/mytable"
        # )
        tab=_d.Table.from_table_arn(
            self,
            "ddb",
            table_arn="arn:aws:dynamodb:us-east-1:325764798866:table/mytable"
        )
        try:
            with open("serverless_stack/dynlambda.py",mode="r") as f:
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
                "LOG_LEVEL": "INFO",
                "DDB_TABLE_NAME": f"{dyn_table.table_name}"# CREATES ENVIRONMENT VARIABLES
            },
            reserved_concurrent_executions=1,
            timeout=core.Duration.seconds(3),
            function_name="dbcode"
        )
        
        # log_fn.role(
        #     _iam.IRole.add_managed_policy(self,
        #                                  policy="AmazonS3ReadOnlyAccess")
        # )
        
        log_fn.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess")
        )
        
        #_iam.IRole.
        print(log_fn.function_name)
        print(log_fn.role)
        
        dyn_table.grant_write_data(log_fn)
        