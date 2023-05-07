from aws_cdk import Stack
from constructs import Construct
from cdk_eks_blueprint.cluster.eks_cluster import EKSCluster
from cdk_eks_blueprint.cluster.controller_plane import ControllerPlane
from cdk_eks_blueprint.cluster.fargate_profile import FargateProfile
from aws_cdk import aws_ec2 as ec2, aws_eks as eks
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer


class ServerlessEKS(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        cluster_name: str,
        k8s_version: str,
        fargate_profile_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        eks_controller = ControllerPlane(
            core_dns_compute_type="FARGATE",  # Need to be FARGATE if pods of kube-system run on fargate
            cluster_name=cluster_name,
            version=k8s_version,
            kubectl_layer=KubectlV24Layer(self, "KubectlV24Layer"),
        )
        fargate_profile = FargateProfile(
            fargate_profile_name=fargate_profile_name,
            selectors=[
                eks.Selector(namespace="kube-system"),
                eks.Selector(namespace="default"),
            ],
        )
        EKSCluster(
            self,
            f"{cluster_name}",
            controller_plane=eks_controller,
            fargate_profiles=[fargate_profile],
        )
