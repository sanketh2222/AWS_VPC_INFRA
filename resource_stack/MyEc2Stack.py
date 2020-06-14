from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_s3 as _s3

class MyEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        # reading the bootstrap file
        with open("Bootstrap_scripts/install_httpd.sh") as f:
            user_data=f.read()
            #print(user_data)
            
            
        
        # getting the latest AMI id
        
        linux_image=_ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )
        
        myvpc=_ec2.Vpc.from_lookup(
            self,
            "MyDefVpc",
            is_default=True
        )
        
        
        prod_configs=self.node.try_get_context('envs')['prod']
        # print(prod_configs['ec2_configs']['image'])
        # print(prod_configs['region'])
        
        
        
        
        webserver2=_ec2.Instance(
            self,
            "webserver3",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="WebServer02",
            machine_image=linux_image,
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
            value=webserver2.instance_id
        )
        
        
        #additional policy (insatnce profile) to ec2 instances
        
        webserver2.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )
        
    
        
        
        webserver2.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )
        )
        
        
        # outputs IP address of webserver
        
        core.CfnOutput(
            self,
            "webserverip",
            value=f"http://{webserver2.instance_public_ip}",
            description=" IP address of Webserver02"
        )
        
        # open traffic at port 80
        
        webserver2.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Opening port 80 Traffic for webserver02"
        )
        
        
        
        