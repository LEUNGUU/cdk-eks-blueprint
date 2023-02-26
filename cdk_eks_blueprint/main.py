from aws_cdk import Stack
from constructs import Construct
from control_plane.cluster import EKSCluster


class MyStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, cluster_name, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        EKSCluster(
            self,
            "ekstest",
            cluster_name=cluster_name,
        )
