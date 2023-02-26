from aws_cdk import aws_eks as eks
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import Duration
from constructs import Construct


class EKSCluster(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        cluster_name: str = "EKSCluster",
        vpc_id: str = "",
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)
        if vpc_id:
            vpc = ec2.Vpc.from_lookup(self, "CustomVPC", vpc_id=vpc_id)
        else:
            vpc = ec2.Vpc(
                self,
                "VPC",
                max_azs=2,
                ip_addresses=ec2.IpAddresses.cidr("172.31.0.0/16"),
                subnet_configuration=[
                    ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PUBLIC, name="Public", cidr_mask=20
                    ),
                    ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                        name="Private",
                        cidr_mask=22,
                    ),
                ],
                nat_gateways=1,
            )
        self.cluster = eks.Cluster(
            self,
            "EKSCluster",
            version=eks.KubernetesVersion.V1_21,
            alb_controller=eks.AlbControllerOptions(
                version=eks.AlbControllerVersion.V2_4_1
            ),
            cluster_logging=[
                eks.ClusterLoggingTypes.API,
                eks.ClusterLoggingTypes.AUTHENTICATOR,
                eks.ClusterLoggingTypes.CONTROLLER_MANAGER,
                eks.ClusterLoggingTypes.AUDIT,
            ],
            core_dns_compute_type=eks.CoreDnsComputeType.EC2,  # or Fargate
            endpoint_access=eks.EndpointAccess.PUBLIC_AND_PRIVATE,
            cluster_name=cluster_name,
            output_cluster_name=True,
            vpc=vpc,
        )
        self.cluster.add_auto_scaling_group_capacity(
            "EKSAutoScalingGroup",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM
            ),
            key_name="macYu",
            max_capacity=5,
            min_capacity=1,
            signals=autoscaling.Signals.wait_for_all(timeout=Duration.minutes(10)),
        )
        # Create a launch Template first
        launch_template = ec2.CfnLaunchTemplate(
            self,
            "EKSManagedNodeGroupLaunchTemplate",
            launch_template_data=ec2.CfnLaunchTemplate.LaunchTemplateDataProperty(
                block_device_mappings=[
                    ec2.CfnLaunchTemplate.BlockDeviceMappingProperty(
                        device_name="xvdb",
                        ebs=ec2.CfnLaunchTemplate.EbsProperty(
                            delete_on_termination=True,
                            encrypted=True,
                            volume_size=50,
                            volume_type="gp3",
                            iops=8000,
                            throughput=500,
                        ),
                    ),
                ]
            ),
        )
        self.cluster.add_nodegroup_capacity(
            "EKSManagedNodeGroup",
            nodegroup_name="EKSManagedNodeGroup",
            ami_type=eks.NodegroupAmiType.AL2_X86_64,
            capacity_type=eks.CapacityType.ON_DEMAND,
            desired_size=2,
            min_size=2,
            max_size=5,
            launch_template_spec=eks.LaunchTemplateSpec(
                id=launch_template.ref,
                version=launch_template.attr_latest_version_number,
            ),
            # disk_size=50,
            instance_types=[
                ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM)
            ],
        )
