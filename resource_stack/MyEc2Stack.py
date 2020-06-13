from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core

class MyEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        myvpc=_ec2.Vpc.from_lookup(
            self,
            "MyDefVpc",
            is_default=True
        )
        
        
        prod_configs=self.node.try_get_context('envs')['prod']
        print(prod_configs['ec2_configs']['image'])
        print(prod_configs['region'])
        
        webserver=_ec2.Instance(
            self,
            "Webserver",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="WebServer01",
            machine_image=_ec2.MachineImage.generic_linux(
            {
                prod_configs['region']:prod_configs['ec2_configs']['image']
            }
            ),
            key_name="irkp",
            vpc=myvpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC,
                
            )
        )
        
        core.CfnOutput(
            self,
            "ec2out",
            value=webserver.instance_id
        )