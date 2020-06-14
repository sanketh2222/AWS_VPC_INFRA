from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core

class MyEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # reading the bootstrap file
        with open("Bootstrap_scripts/install_httpd.sh") as f:
            user_data=f.read()
            print(user_data)
        
        myvpc=_ec2.Vpc.from_lookup(
            self,
            "MyDefVpc",
            is_default=True
        )
        
        
        prod_configs=self.node.try_get_context('envs')['prod']
        # print(prod_configs['ec2_configs']['image'])
        # print(prod_configs['region'])
        
        webserver1=_ec2.Instance(
            self,
            "Webserver1",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="WebServer02",
            machine_image=_ec2.MachineImage.generic_linux(
            {
                prod_configs['region']:prod_configs['ec2_configs']['image']
            }
            ),
            key_name="irkp",
            vpc=myvpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC,
                
            ),
            user_data=_ec2.UserData.custom(user_data)
        )
        
        core.CfnOutput(
            self,
            "ec2out",
            value=webserver1.instance_id
        )
        
        
        
        # outputs IP address of webserver
        
        core.CfnOutput(
            self,
            "webserverip",
            value=f"http://{webserver1.instance_public_ip}",
            description=" IP address of Webserver01"
        )
        
        # open traffic at port 80
        
        webserver1.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Opening port 80 Traffic for webserver01"
        )
        
        