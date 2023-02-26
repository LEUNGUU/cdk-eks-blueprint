from typing import List, Union, Dict
from dataclasses import dataclass
from constructs import Construct
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
)


@dataclass
class Validations:
    def __post_init__(self):
        """Run validation methods if declared.
        The validation method can be a simple check
        that raises ValueError or a transformation to
        the field value.
        The validation is performed by calling a function named:
            `validate_<field_name>(self, value, field) -> field.type`
        """
        for name, field in self.__dataclass_fields__.items():
            if method := getattr(self, f"validate_{name}", None):
                setattr(self, name, method(getattr(self, name), field=field))


@dataclass
class DefaultCapacity(Validations):
    node_number: int
    node_type: Union[str, ec2.InstanceType]
    capacity_type: Union[str, eks.DefaultCapacityType]

    def validate_node_number(self, value: int, **_) -> int:
        if not isinstance(value, int):
            raise ValueError("node_number must be integer")
        return value

    def validate_node_type(self, value, **_) -> Union[ec2.InstanceType, None]:
        if not (is_str := isinstance(value, str)) and not (
            is_obj := isinstance(value, ec2.InstanceType)
        ):
            raise ValueError("node_type must be string or ec2.InstanceType")
        if is_str:
            instance_class, instance_size = value.upper().split(".")
            if (
                instance_class not in ec2.InstanceClass.__members__
                or instance_size not in ec2.InstanceSize.__members__
            ):
                raise ValueError("node_type should be valid ec2 instance type")
            return ec2.InstanceType.of(
                getattr(ec2.InstanceClass, instance_class),
                getattr(ec2.InstanceSize, instance_size),
            )
        if is_obj:  # type: ignore
            return value

    def validate_capacity_type(
        self, value, **_
    ) -> Union[eks.DefaultCapacityType, None]:
        if not (is_str := isinstance(value, str)) and not (
            is_obj := isinstance(value, eks.CapacityType)
        ):
            raise ValueError("capacity_type must be string or eks.CapacityType")
        if is_str:
            capacity_type = value.upper()
            if capacity_type not in eks.DefaultCapacityType.__members__:
                raise ValueError("capacity_type should be either nodegroup or ec2")
            return getattr(eks.DefaultCapacityType, capacity_type)
        if is_obj:  # type: ignore
            return value  # type: ignore


@dataclass
class ControlPlaneParams(Validations, Construct):
    # General config
    cluster_name: str
    k8s_version: Union[str, eks.KubernetesVersion]
    secrets_encryption_key: str
    endpoint_access: eks.EndpointAccess
    master_role: Union[str, iam.Role]  # use from to change to IRole
    role: str
    cluster_logging: List[eks.ClusterLoggingTypes]
    core_dns_compute_type: eks.CoreDnsComputeType
    service_ipv4_cidr: str
    security_group: str
    vpc: ec2.Vpc
    vpc_subnets: str

    # Nodegroup related
    default_capacity: DefaultCapacity

    # lambda
    kubectl_lambda_role: str
    awscli_layer: str
    cluster_handler_environment: str
    cluster_handler_security_group: str
    kubectl_environment: str
    kubectl_layer: str
    kubectl_memory: str
    on_event_layer: str
    place_cluster_handler_in_vpc: str

    # plugin
    alb_controller: eks.AlbControllerOptions

    # output
    output_config_command: bool
    output_cluster_name: bool

    tags: Dict[str, str]

    def validate_master_role(self, value, **_) -> None:
        if not (is_str := isinstance(value, str)) and not (
            is_obj := isinstance(value, iam.Role)
        ):
            raise ValueError("master_role must be string or iam.Role")

    def validate_k8s_version(self, value, **_) -> Union[None, eks.KubernetesVersion]:
        if not (is_str := isinstance(value, str)) and not (
            is_obj := isinstance(value, eks.KubernetesVersion)
        ):
            raise ValueError("k8s_version must be string or eks.KubernetesVersion")
        if is_str:  # 1.21
            value = f'V{value.replace(".", "_")}'
            return getattr(eks.KubernetesVersion, value)
        if is_obj: # type: ignore
            return value


if __name__ == "__main__":
    try:
        dc = DefaultCapacity(
            node_number=2, node_type="t3.medium", capacity_type="nodegroup"
        )
        print(dc.node_number, dc.node_type, dc.capacity_type)
    except ValueError as e:
        raise e
