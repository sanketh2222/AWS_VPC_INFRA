from aws_cdk import aws_ec2 as _ec2
from aws_cdk import core
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_autoscaling as _au 
from aws_cdk import  aws_elasticloadbalancingv2 as _elb


class MyEc2AsgStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        
        # reading the bootstrap file
        try:
            with open("app_db_stack/UserData/deploy.sh") as f:
                user_data=f.read()
                print(user_data)
        except OSError:
            print("Cannot find path specified")
            
            
        linux_image=_ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )
        
        
      
        
       
       #creating an application load balancer
        alb=_elb.ApplicationLoadBalancer(
            self,
            "MyLoadBalancer",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="MyAppLoadBalancer"
        )
            
        # opening port 80
        alb.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Opening port 80 for ALB"
        )
        
        # Adding listner
        
        listner=alb.add_listener(
            "alblistner",
            port=80,
            open=True
        )
        
        webserver_role=_iam.Role(
            self,
            "WebIdentityRole",
            assumed_by=_iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                _iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonS3ReadOnlyAccess"
                )
            ]
        )
        
       
        self.web_Server_asg=_au.AutoScalingGroup(
            self,
            "MyASG",
            vpc=vpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PRIVATE
            ),
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            machine_image=linux_image,
            min_capacity=2,
            max_capacity=2,
            role=webserver_role,
            user_data=_ec2.UserData.custom(user_data)
        )
        
        self.web_Server_asg.connections.allow_from(alb,_ec2.Port.tcp(80),
                                              description="Allow traffic on port 80 from ALB")
        
        
        
        listner.add_targets("listnerid", port=80, targets=[self.web_Server_asg])
        
        
        
        
        
        
        core.CfnOutput(
            self,
            "Loadbalurl",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Load Balancer URL"
        )