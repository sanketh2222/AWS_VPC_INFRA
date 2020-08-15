from aws_cdk import core
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_events as _events
from aws_cdk import aws_events_targets as _target


import json
import os


class MyLambdaAsCronStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # code begins
        #importing existing bucket
        s3bkt=_s3.Bucket.from_bucket_name(self,
                                          "mybkt",
                                          bucket_name="mybuck2809")
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
        
        # 6pm everyday rule
        
        lambda_event=_events.Rule(
            self,
            "dailysch",
            description="run at 6pm everyday",
            schedule=_events.Schedule.cron(
                minute="00",
                hour="18",
                week_day="MON-FRI",
                year="*"
            )
        )
        
        base_event=_events.Rule(
            self,
            "base",
            enabled=True,
            rule_name="base_rule",
            schedule=_events.Schedule.rate(core.Duration.minutes(10))
        )
        
        
        # add these rules created to lambda function
        
        base_event.add_target(_target.LambdaFunction(log_fn))
        lambda_event.add_target(_target.LambdaFunction(log_fn))