from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_apigateway as _apig
from aws_cdk import aws_cloudwatch as _cw
from aws_cdk import aws_sns as _sns
from aws_cdk import aws_sns_subscriptions as _subs
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_cloudwatch_actions as _cwact
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam



import json
import os


class MonitoringStack(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        
        ops_team = _sns.Topic(self,
                            "konstoneOpsTeam",
                            display_name="KonStone 24x7 On Watsapp Support",
                            topic_name="OpsTeam"
                            )
        
        ops_team.add_subscription(
            _subs.EmailSubscription(
                email_address="ssankethboss061@gmail.com"
            )
        )
        try:
            with open("Bootstrap_scripts/install_httpd.sh") as f:
                user_data=f.read()
                print("file read \n")
        except OSError:
            print("file not found")
            
        try:
            with open("serverless_stack/hello.py",mode="r") as f:
                lambda_code=f.read()
                print("file read\n")
        except OSError:
            print("file not found")
          
          
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
        
        #default vpc
        myvpc = _ec2.Vpc.from_lookup(
            self,
             "VPC",
            is_default=True
            #vpc_id ="vpc-e2aab998"
        )
        
        #prod_configs=self.node.try_get_context('envs')['prod']
        
        #print(prod_configs)
        
        linux_image=_ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )
        
        webserver2=_ec2.Instance(
            self,
            "webserver3",
            instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
            instance_name="WebServer021",
            machine_image=linux_image,
            key_name="irkp",
            vpc=myvpc,
            vpc_subnets=_ec2.SubnetSelection(
                subnet_type=_ec2.SubnetType.PUBLIC,
                
            ),
            user_data=_ec2.UserData.custom(user_data)
        )
        
        webserver2.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )
        
        # open traffic at port 80
        
        webserver2.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80),
             description="Opening port 80 Traffic for webserver02"
        )
        
        # create a metric for avg cpu utlilization < 10%
        avg_cpu_metric=_cw.Metric(
            metric_name="CPUUtilization",
            namespace="AWS/EC2",
            dimensions={
                "InstanceId":webserver2.instance_id
            },
            period=core.Duration.minutes(2)
        )
        
        # create a alarm
        cpu_alarm=_cw.Alarm(
            self,
            "cpualarm",
            metric=avg_cpu_metric,
            evaluation_periods=1,
            threshold=10,
            period=core.Duration.minutes(2),
            actions_enabled =True,
            alarm_description="avg cpu utilization",
            alarm_name ="avg_cpu1",
            comparison_operator=_cw.ComparisonOperator.LESS_THAN_OR_EQUAL_TO_THRESHOLD,
            datapoints_to_alarm=1,
            treat_missing_data=_cw.TreatMissingData.NOT_BREACHING
            
        )
        
        
        #create action to sns topic for first metric alarm
        cpu_alarm.add_alarm_action(
            _cwact.SnsAction(
                ops_team
            )
        )
        
        
        # create an alarm for failure of lambda function
        lmbda_alarm=_cw.Alarm(
            self,
            "lambdaAlrm",
            metric=log_fn.metric_all_errors(),
            threshold=2,
            period=core.Duration.minutes(2),
            alarm_name ="avg_cpu",
            datapoints_to_alarm=1,
            evaluation_periods=1
            
            
            
        )
        
        lmbda_alarm.add_alarm_action(
            _cwact.SnsAction(
                ops_team
            )
        )