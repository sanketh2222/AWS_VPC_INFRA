from aws_cdk import core
from aws_cdk import aws_dynamodb as _d

import json
import os


class MyDynamoStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        dyn_table=_d.Table(
            self,
            "demotable",
            table_name="mytable",
            partition_key=_d.Attribute(
                name="id",
                type=_d.AttributeType.NUMBER
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )
        
        # _d.Attribute(
        #     name="Name",
        #     type=_d.AttributeType.STRING
        # )
        
        # _d.Attribute(
        #     name="Age",
        #     type=_d.AttributeType.NUMBER
        # )