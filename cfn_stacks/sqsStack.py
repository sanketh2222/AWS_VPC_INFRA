from aws_cdk import core
from aws_cdk import aws_sns as _sns
from  aws_cdk import aws_sqs as _sqs



class SQSStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # start coding
        
        myqueue=_sqs.Queue(
            self,
            "MyQ",
            queue_name="MyQ.fifo",
            fifo=True,
            max_message_size_bytes=4096,
            visibility_timeout=core.Duration.seconds(30),
            retention_period=core.Duration.days(1)
            #encryption=_sqs.QueueEncryption.KMS
            
        )
        
        core.CfnOutput(
            self,
            "Qdetails",
             value=f"{myqueue.queue_name}"
        )