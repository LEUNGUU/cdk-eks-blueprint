from typing import Optional, Dict, List, Any, Union
from ._params_validation import Validation
from dataclasses import dataclass, field
from aws_cdk.aws_autoscaling import (
    BlockDevice,
    GroupMetrics,
    HealthCheck,
    Monitoring,
    Signals,
    TerminationPolicy,
    UpdatePolicy,
    NotificationConfiguration,
)
from aws_cdk import Duration, aws_ec2 as ec2, aws_eks as eks


@dataclass
class EKSManagedNodeGroup(Validation):
    auto_scaling_group_name: str
    instance_type: str = "t3.medium"
    bootstrap_enabled: bool = True
    bootstrap_options: Optional[Dict[str, Any]] = None
    machine_image_type: str = "amazon_linux_2"
    map_role: bool = True
    spot_interrupt_handler: bool = True
    allow_all_outbound: bool = True
    associate_public_ip_address: bool = False
    block_devices: Optional[Union[BlockDevice, Dict[str, Any]]] = None
    capacity_rebalance: Optional[bool] = False
    cooldown: Optional[Duration] = Duration.minutes(5)
    desired_capacity: Union[int, float, None] = None
    group_metrics: Optional[List[GroupMetrics]] = None
    health_check: Optional[HealthCheck] = HealthCheck.ec2()
    ignore_unmodified_size_properties: Optional[bool] = True
    instance_monitoring: Optional[Monitoring] = Monitoring.DETAILED
    key_name: Optional[str] = None
    max_capacity: Union[int, float, None] = None
    max_instance_lifetime: Optional[Duration] = None
    min_capacity: Union[int, float, None] = 1
    new_instances_protected_from_scale_in: Optional[bool] = False
    notifications: Optional[
        List[Union[NotificationConfiguration, Dict[str, Any]]]
    ] = None
    signals: Optional[Signals] = None
    spot_price: Optional[str] = None
    termination_policies: Optional[List[TerminationPolicy]] = field(
        default_factory=lambda: [TerminationPolicy.DEFAULT]
    )
    update_policy: Optional[UpdatePolicy] = None
    vpc_subnets: Union[ec2.SubnetSelection, Dict[str, Any], None] = None

    def validate_instance_type(self, value: str, **_) -> Union[ec2.InstanceType, None]:
        if not isinstance(value, str):
            raise ValueError("instance_type must be string")
        instance_class, instance_size = value.upper().split(".")
        if (
            instance_class not in ec2.InstanceClass.__members__
            or instance_size not in ec2.InstanceSize.__members__
        ):
            raise ValueError("instance_type should be valid ec2 instance type")
        return ec2.InstanceType.of(
            getattr(ec2.InstanceClass, instance_class),
            getattr(ec2.InstanceSize, instance_size),
        )

    def validate_machine_image_type(
        self, value: str, **_
    ) -> Union[eks.MachineImageType, None]:
        if not isinstance(value, str):
            raise ValueError("machine_image_type must be string")
        if value.upper() not in eks.MachineImageType.__members__:
            raise ValueError(
                "machine_image_type should be amazon_linux_2 or bottlerocket"
            )
        return getattr(eks.MachineImageType, value.upper())


if __name__ == "__main__":
    eks_managed_node_group = EKSManagedNodeGroup(auto_scaling_group_name="test")
