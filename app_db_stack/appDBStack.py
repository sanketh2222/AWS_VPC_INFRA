from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_rds as _rds
from aws_cdk import core


class RdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,vpc,securitygroups, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # start coding
        
        mydb=_rds.DatabaseInstance(
            self,
            "myrds",
            master_username="MyRDSInstance",
            database_name="MySpaceX",
            engine=_rds.DatabaseInstanceEngine.MYSQL,
            allocated_storage=30,
            cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
            deletion_protection=False,
            port=3306,
            instance_type=_ec2.InstanceType.of(
                 
                _ec2.InstanceClass.BURSTABLE2,
                _ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            removal_policy=core.RemovalPolicy.DESTROY,
            delete_automated_backups=True,
            backup_retention=core.Duration.days(7)
            
            
        )
        
        for sg in securitygroups: 
            mydb.connections.allow_default_port_from(
                sg,description=" Allow connection for EC2 on port 3306 of RDS DB"
            )
            
            
        core.CfnOutput(
            self,
            "DBconnection",
            value=f"mysql -h {mydb.db_instance_endpoint_address} -P 3306 -u MyRDSInstance -p",
            description=" command to connect to RDS db"
        )