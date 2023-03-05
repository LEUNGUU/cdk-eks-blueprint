from constructs import Construct
from aws_cdk import aws_ec2 as ec2


class VPC(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        vpc_id: str = "",
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)
        if vpc_id:
            self.vpc = ec2.Vpc.from_lookup(self, "CustomizedVPC", vpc_id=vpc_id)
        else:
            self.vpc = ec2.Vpc(
                self,
                "EKSVPC",
                max_azs=2,
                ip_addresses=ec2.IpAddresses.cidr("172.31.0.0/16"),
                subnet_configuration=[
                    ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PUBLIC,
                        name="Public",
                        cidr_mask=22,
                    ),
                    ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                        name="Private",
                        cidr_mask=20,
                    ),
                ],
                nat_gateways=1,
            )
