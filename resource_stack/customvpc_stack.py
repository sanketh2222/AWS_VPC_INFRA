from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_kms as _kms
from aws_cdk import aws_s3 as _s3
from aws_cdk import core

class Customvpc(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        
        prod_configs=self.node.try_get_context('envs')['prod']
        mask=prod_configs['vpc_configs']['mask']
        
        Custom_vpc=_ec2.Vpc(
            self,
            "Vpcid",
             cidr=prod_configs['vpc_configs']['vpc_cidr'],
             max_azs=2,
             subnet_configuration=[
                 _ec2.SubnetConfiguration(
                     name="PrivateSubnet", subnet_type=_ec2.SubnetType.PRIVATE, cidr_mask=prod_configs['vpc_configs']['mask']
                 ),
                 _ec2.SubnetConfiguration(
                     name="PublicSubnet",  subnet_type=_ec2.SubnetType.PUBLIC, cidr_mask=prod_configs['vpc_configs']['mask']
                 ),
                 _ec2.SubnetConfiguration(
                     name="DBSubnet",  subnet_type=_ec2.SubnetType.ISOLATED, cidr_mask=prod_configs['vpc_configs']['mask']
                 )
             ]
        )
        
        
        # print(mask)
        
        core.CfnOutput(
            self,
            "vpcout",
             value=Custom_vpc.vpc_id,
            export_name="myvpcout"
        )
        
        core.Tag.add(Custom_vpc,"Owner","Sanketh")
        
        mybucket=_s3.Bucket(
            self,
            "mybuck"
        )
        
        core.Tag.add(mybucket,"Owner","Sanketh")
        
        
        '''
        vpc_id2=_ec2.Vpc.from_lookup(
            self,
            "myvpc2",
            vpc_id="vpc-e2aab998"
        )
        '''
        
        '''
        core.CfnOutput(
            self,
            "vpc2id",
            value=vpc_id2.vpc_id
        )
        '''
        
        '''
        peervpc=_ec2.CfnVPCPeeringConnection(
            self,
            "vpcpeer",
            vpc_id=Custom_vpc.vpc_id,    #requester vpc id (custom vpc)
            peer_vpc_id=vpc_id2.vpc_id  #acceptor vpc id (default vpc)
        )
        
        '''