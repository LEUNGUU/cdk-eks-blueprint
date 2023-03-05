from typing import List, Union, Dict
from ipaddress import ip_network
from dataclasses import dataclass
from aws_cdk import (
    aws_eks as eks,
    aws_ec2 as ec2,
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
    node_type: str
    capacity_type: str

    def validate_node_number(self, value: int, **_) -> int:
        if not isinstance(value, int):
            raise ValueError("node_number must be integer")
        return value

    def validate_node_type(self, value, **_) -> Union[ec2.InstanceType, None]:
        if not isinstance(value, str):
            raise ValueError("node_type must be string")
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

    def validate_capacity_type(
        self, value, **_
    ) -> Union[eks.DefaultCapacityType, None]:
        if not isinstance(value, str):
            raise ValueError("capacity_type must be string or eks.CapacityType")
        capacity_type = value.upper()
        if capacity_type not in eks.DefaultCapacityType.__members__:
            raise ValueError("capacity_type should be either nodegroup or ec2")
        return getattr(eks.DefaultCapacityType, capacity_type)


@dataclass
class ControlPlaneParams(Validations):
    # General config
    k8s_version: str
    endpoint_access: str
    cluster_logging: List[str]
    core_dns_compute_type: str

    # Nodegroup related
    default_capacity: DefaultCapacity

    tags: Dict[str, str]

    def validate_k8s_version(self, value, **_) -> Union[None, eks.KubernetesVersion]:
        if not (is_str := isinstance(value, str)):
            raise ValueError("k8s_version must be string")
        if is_str:  # 1.21
            value = f'V{value.replace(".", "_")}'
            return getattr(eks.KubernetesVersion, value)

    def validate_endpoint_access(
        self, value, **_
    ) -> Union[None, eks.EndpointAccess, str]:
        if not (is_str := isinstance(value, str)) and not (
            is_obj := isinstance(value, eks.EndpointAccess)
        ):
            raise ValueError("endpoint_access must be string or eks.EndpointAccess")
        if is_str:
            if value.upper() in ["PRIVATE", "PUBLIC", "PUBLIC_AND_PRIVATE"]:
                return getattr(eks.EndpointAccess, value.upper())
            else:
                try:
                    ip_network(value)
                    # return value # value should be valid ip cidr
                    return eks.EndpointAccess().only_form(value)
                except Exception as e:
                    raise e
        if is_obj:  # type: ignore
            return value

    def validate_cluster_logging(
        self, value, **_
    ) -> Union[None, List[eks.ClusterLoggingTypes]]:
        if not (is_lst := isinstance(value, list)):
            raise ValueError("cluster_logging must be list of string")
        full_set = set(
            ["API", "AUDIT", "AUTHENTICATOR", "CONTROLLER_MANAGER", "SCHEDULER"]
        )
        if is_lst:
            if set(value).issubset(full_set):
                res = []
                for item in value:
                    res.append(getattr(eks.ClusterLoggingTypes, item))
                    return res
            else:
                raise ValueError(
                    "Log Type must be one or some of [API, AUDIT, AUTHENTICATOR, CONTROLLER_MANAGER, SCHEDULER]"
                )

    def validate_core_dns_compute_type(
        self, value, **_
    ) -> Union[None, eks.CoreDnsComputeType]:
        if not isinstance(value, str):
            raise ValueError("core_dns_compute_type must be string")
        if value.upper() not in ["EC2", "FARGATE"]:
            raise ValueError("core_dns_compute_type must be one of [EC2, FARGATE]")
        return getattr(eks.CoreDnsComputeType, value)

    def validate_default_capacity(self, value, **_) -> None:
        if not isinstance(value, DefaultCapacity):
            raise ValueError("default_capacity must be DefaultCapacity")


if __name__ == "__main__":
    try:
        dc = DefaultCapacity(
            node_number=2, node_type="t3.medium", capacity_type="nodegroup"
        )
        cpp = ControlPlaneParams(
            k8s_version="1.21",
            endpoint_access="public_and_private",
            cluster_logging=["API"],
            core_dns_compute_type="EC2",
            default_capacity=dc,
            tags={}
        )
        print(dc.node_number, dc.node_type, dc.capacity_type)
        print(cpp.k8s_version, cpp.endpoint_access)
    except ValueError as e:
        raise e
