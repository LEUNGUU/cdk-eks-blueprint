from typing import List, Union, Dict, Optional, Any
from semver import VersionInfo
from ipaddress import ip_network
from dataclasses import dataclass, field
from ._params_validation import Validation
from aws_cdk import (
    Size,
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_kms as kms,
)


@dataclass
class ControllerPlane(Validation):
    cluster_name: str

    kubectl_lambda_role: Optional[iam.IRole] = None
    awscli_layer: Optional[_lambda.ILayerVersion] = None
    cluster_handler_environment: Optional[Dict[str, str]] = None
    cluster_handler_security_group: Optional[ec2.ISecurityGroup] = None
    kubectl_environment: Optional[Dict[str, str]] = None
    kubectl_layer: Optional[_lambda.ILayerVersion] = None
    kubectl_memory: Optional[Size] = None
    masters_role: Optional[iam.IRole] = None
    on_event_layer: Optional[_lambda.ILayerVersion] = None
    place_cluster_handler_in_vpc: Optional[bool] = None
    secrets_encryption_key: Optional[kms.IKey] = None
    service_ipv4_cidr: Optional[str] = None
    role: Optional[iam.IRole] = None
    security_group: Optional[ec2.ISecurityGroup] = None
    vpc: Optional[ec2.IVpc] = None
    vpc_subnets: Optional[List[Union[ec2.SubnetSelection, Dict[str, Any]]]] = None
    tags: Optional[Dict[str, str]] = None

    default_capacity: Union[int, float, None] = 0
    default_capacity_instance: Optional[str] = "t3.medium"
    default_capacity_type: Optional[str] = "nodegroup"
    cluster_logging: Optional[List[str]] = field(
        default_factory=lambda: ["API", "CONTROLLER_MANAGER", "AUDIT"]
    )
    core_dns_compute_type: Optional[str] = "EC2"
    endpoint_access: Optional[str] = "PUBLIC_AND_PRIVATE"
    alb_controller: str = "2.4.1"
    output_masters_role_arn: Optional[bool] = True
    output_cluster_name: Optional[bool] = True
    output_config_command: Optional[bool] = True
    prune: Optional[bool] = True
    version: str = "1.21"

    def validate_version(self, value, **_) -> Union[None, eks.KubernetesVersion]:
        if not isinstance(value, str):
            raise ValueError("k8s_version must be string")
        value = f'V{value.replace(".", "_")}'
        return getattr(eks.KubernetesVersion, value)

    def validate_endpoint_access(self, value, **_) -> Union[None, eks.EndpointAccess]:
        if not isinstance(value, str):
            raise ValueError("endpoint_access must be string")
        if value.upper() in ["PRIVATE", "PUBLIC", "PUBLIC_AND_PRIVATE"]:
            return getattr(eks.EndpointAccess, value.upper())
        else:
            try:
                ip_network(value)
                # return value # value should be valid ip cidr
                return eks.EndpointAccess().only_form(value)
            except Exception as e:
                raise e

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

    def validate_alb_controller(
        self, value, **_
    ) -> Union[eks.AlbControllerOptions, None]:
        if not isinstance(value, str) or not VersionInfo.is_valid(value):
            raise ValueError("alb_controller_version must be valid version string")
        versionNumber = f"V{value.replace('.', '_')}"
        try:
            return eks.AlbControllerOptions(
                version=getattr(eks.AlbControllerVersion, versionNumber)
            )
        except Exception as e:
            raise e

    def validate_default_capacity_instance(
        self, value, **_
    ) -> Union[ec2.InstanceType, None]:
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

    def validate_default_capacity_type(
        self, value, **_
    ) -> Union[eks.DefaultCapacityType, None]:
        if not isinstance(value, str):
            raise ValueError("capacity_type must be string or eks.CapacityType")
        capacity_type = value.upper()
        if capacity_type not in eks.DefaultCapacityType.__members__:
            raise ValueError("capacity_type should be either nodegroup or ec2")
        return getattr(eks.DefaultCapacityType, capacity_type)

    def validate_tags(self, value, **_) -> Union[Dict[str, str], None]:
        if not value:
            value = {}
        if not isinstance(value, dict):
            raise ValueError("tags must be dict of strings")
        value.update({"owner": "Managed by CDK"})
        return value
