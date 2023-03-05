# pyright: reportUndefinedVariable=false, reportGeneralTypeIssues=false
from typing import List, Dict
from aws_cdk import aws_eks as eks
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import Duration
from constructs import Construct
from vpc import VPC
from param_wrapper import ControlPlaneParams, DefaultCapacity



class EKSCluster(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        cluster_name: str = "EKSCluster",
        k8s_version: str = "1.21",
        endpoint_access: str = "PUBLIC_AND_PRIVATE",
        cluster_logging: List[str] = ["API", "CONTROLLER_MANAGER", "AUDIT"],
        core_dns_compute_type: str = "EC2",
        default_node_number: int = 0,
        default_node_type: str = "t3.medium",
        default_capacity_type: str = "nodegroup",
        vpc_id: str = "",
        output_cluster_name: bool = True,
        output_config_command: bool = True,
        tags: Dict[str, str] = {},
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)
        default_tags = {"owner": "Managed by CDK"}
        default_tags.update(tags)
        dc = DefaultCapacity(
            node_number=default_node_number,
            node_type=default_node_type,
            capacity_type=default_capacity_type
        )
        cpp = ControlPlaneParams(
            k8s_version=k8s_version,
            endpoint_access=endpoint_access,
            cluster_logging=cluster_logging,
            core_dns_compute_type=core_dns_compute_type,
            default_capacity=dc,
            tags=default_tags
        )
        vpc = VPC(
            self,
            "EKSVPC",
            vpc_id=vpc_id if vpc_id else ""
        )
        self.cluster = eks.Cluster(
            self,
            "EKSCluster",
            version=cpp.k8s_version,
            alb_controller=eks.AlbControllerOptions(
                version=eks.AlbControllerVersion.V2_4_1
            ),
            cluster_logging=cpp.cluster_logging,
            core_dns_compute_type=cpp.core_dns_compute_type,
            endpoint_access=cpp.endpoint_access,
            cluster_name=cluster_name,
            output_cluster_name=output_cluster_name,
            output_config_command=output_config_command,
            vpc=vpc.vpc,
        )
        self.cluster.add_auto_scaling_group_capacity(
            "EKSAutoScalingGroup",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM
            ),
            key_name="macYu",
            kax_capacity=5,
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
