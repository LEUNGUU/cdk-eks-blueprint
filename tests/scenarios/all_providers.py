from aws_cdk import Stack
from constructs import Construct
from cdk_eks_blueprint.cluster.eks_cluster import EKSCluster
from cdk_eks_blueprint.cluster.managed_node_group import EKSManagedNodeGroup
from cdk_eks_blueprint.cluster.self_managed_node_group import SelfManagedNodeGroup
from cdk_eks_blueprint.cluster.controller_plane import ControllerPlane
from cdk_eks_blueprint.cluster.fargate_profile import FargateProfile
from aws_cdk import aws_ec2 as ec2, aws_eks as eks
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer


class AllProviders(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        cluster_name: str,
        k8s_version: str,
        auto_scaling_group_name: str,
        min_capacity: str,
        nodegroup_name: str,
        desired_size: int,
        fargate_profile_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        eks_controller = ControllerPlane(
            cluster_name=cluster_name,
            version=k8s_version,
            kubectl_layer=KubectlV24Layer(self, "KubectlV24Layer"),
        )
        managed_nodegroup = EKSManagedNodeGroup(
            auto_scaling_group_name=auto_scaling_group_name,
            min_capacity=min_capacity,
        )
        self_managed_nodegroup = SelfManagedNodeGroup(
            nodegroup_name=nodegroup_name, desired_size=desired_size
        )
        fargate_profile = FargateProfile(
            fargate_profile_name=fargate_profile_name,
            selectors=[eks.Selector(namespace="app")],
        )
        EKSCluster(
            self,
            f"{cluster_name}",
            controller_plane=eks_controller,
            eks_managed_node_groups=[managed_nodegroup],
            self_managed_node_groups=[self_managed_nodegroup],
            fargate_profiles=[fargate_profile],
        )
