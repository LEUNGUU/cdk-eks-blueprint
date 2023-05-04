from typing import List, Union, Dict, Any
from ._params_validation import Validation
from dataclasses import dataclass, field
from aws_cdk import aws_eks as eks, aws_iam as iam, aws_ec2 as ec2


@dataclass
class FargateProfile(Validation):
    fargate_profile_name: str
    selectors: List[Union[Selector, Dict[str, Any]]] = field(
        default_factory=lambda: [
            eks.Selector(namespace="kube-system"),
            eks.Selector(namespace="default"),
        ]
    )
    pod_execution_role: Optional[iam.IRole] = None
    subnet_selection: Union[ec2.SubnetSelection, Dict[str, Any], None] = None
    vpc: Optional[ec2.IVpc] = None
