from aws_cdk import Stack
from constructs import Construct
from cdk_eks_blueprint.cluster.eks_cluster import EKSCluster
from cdk_eks_blueprint.cluster.managed_node_group import EKSManagedNodeGroup
from cdk_eks_blueprint.cluster.self_manage_node_group import SelfManagedNodeGroup
from cdk_eks_blueprint.cluster.controller_plane import ControllerPlane
from aws_cdk import aws_ec2 as ec2, aws_eks as eks
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer


class Captain(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, cluster_name, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        eks_controller = ControllerPlane(
            cluster_name=cluster_name,
            version="1.24",
            kubectl_layer=KubectlV24Layer(self, "KubectlV24Layer"),
        )
        apple = EKSManagedNodeGroup(auto_scaling_group_name="apple", min_capacity=2)
        banana = SelfManagedNodeGroup(nodegroup_name="banana")
        EKSCluster(
            self,
            "ekstest",
            controller_plane=eks_controller,
            eks_managed_node_groups=[apple],
            self_managed_node_group=[banana],
        )
