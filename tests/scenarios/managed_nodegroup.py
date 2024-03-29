from aws_cdk import Stack
from constructs import Construct
from cdk_eks_blueprint.cluster.eks_cluster import EKSCluster
from cdk_eks_blueprint.cluster.managed_node_group import EKSManagedNodeGroup
from cdk_eks_blueprint.cluster.controller_plane import ControllerPlane
from aws_cdk import aws_ec2 as ec2, aws_eks as eks
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer


class ManagedNodeGroupEKS(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        cluster_name: str,
        k8s_version: str,
        auto_scaling_group_name: str,
        min_capacity: int,
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
        EKSCluster(
            self,
            f"{cluster_name}",
            controller_plane=eks_controller,
            eks_managed_node_groups=[managed_nodegroup],
        )
