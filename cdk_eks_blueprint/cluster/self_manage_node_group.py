from typing import Optional, Union, List, Dict, Any
from dataclasses import dataclass, field
from ._params_validation import Validation
from aws_cdk import aws_eks as eks, aws_iam as iam, aws_ec2 as ec2


@dataclass
class SelfManagedNodeGroup(Validation):
    nodegroup_name: str
    ami_type: Optional[str] = "AL2_X86_64"
    capacity_type: Optional[str] = "on_demand"
    desired_size: Union[int, float, None] = 2
    disk_size: Union[int, float, None] = 20
    force_update: Optional[bool] = True
    instance_types: Optional[List[str]] = field(default_factory=lambda: ["t3.medium"])
    labels: Optional[Dict[str, str]] = None
    launch_template_spec: Union[eks.LaunchTemplateSpec, Dict[str, Any], None] = None
    max_size: Union[int, float, None] = 2
    min_size: Union[int, float, None] = 1
    node_role: Optional[iam.IRole] = None
    release_version: Optional[str] = None
    remote_access: Union[eks.NodegroupRemoteAccess, Dict[str, Any], None] = None
    subnets: Union[ec2.SubnetSelection, Dict[str, Any], None] = None
    tags: Optional[Dict[str, str]] = None
    taints: Optional[List[Union[eks.TaintSpec, Dict[str, Any]]]] = None

    def validate_ami_type(self, value: str, **_) -> Union[eks.NodegroupAmiType, None]:
        if not isinstance(value, str):
            raise ValueError("ami_type must be string")
        if value.upper() not in eks.NodegroupAmiType.__members__:
            raise ValueError("ami_type should be valid eks nodegroup ami type")
        return getattr(eks.NodegroupAmiType, value)

    def validate_capacity_type(self, value: str, **_) -> Union[eks.CapacityType, None]:
        if not isinstance(value, str):
            raise ValueError("capacity_type must be string")
        if (exact_value := value.upper()) not in eks.CapacityType.__members__:
            raise ValueError("capacity_type should be valid eks capacity type")
        return getattr(eks.CapacityType, exact_value)

    def validate_instance_types(
        self, value: List[str], **_
    ) -> Union[List[ec2.InstanceType], None]:
        if not isinstance(value, List):
            raise ValueError("instance_type must be List of string")
        res = []
        for instance_type in value:
            instance_class, instance_size = instance_type.upper().split(".")
            if (
                instance_class not in ec2.InstanceClass.__members__
                or instance_size not in ec2.InstanceSize.__members__
            ):
                raise ValueError("instance_type should be valid ec2 instance type")
            res.append(
                ec2.InstanceType.of(
                    getattr(ec2.InstanceClass, instance_class),
                    getattr(ec2.InstanceSize, instance_size),
                )
            )
        return res

    def validate_disk_size(
        self, value: Union[int, float, None], **_
    ) -> Union[int, float, None]:
        if self.launch_template_spec:
            return None
