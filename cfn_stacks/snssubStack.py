from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_rds as _rds
from aws_cdk import core
from aws_cdk import aws_sns as _sns
from  aws_cdk import aws_sqs as _sqs
from aws_cdk import aws_sns_subscriptions as _sub
import json


class SnsSubStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # start coding
        
        MySnsTopic=_sns.Topic(
            self,
            "MyTopic",
            display_name="SNS Topic",
            topic_name="SnsTopic"
        )
        
        MySnsTopic.add_subscription(
            subscription=_sub.EmailSubscription(email_address="sankeths94@gmail.com")
        )
        
        MySnsTopic.add_subscription(
            subscription=_sub.SmsSubscription(phone_number="918310145281")
        )
        
        core.CfnOutput(
            self,
            "topicname",
            value=f"{MySnsTopic.topic_arn}",
            description="Topic arn of Sns Topic"
        )