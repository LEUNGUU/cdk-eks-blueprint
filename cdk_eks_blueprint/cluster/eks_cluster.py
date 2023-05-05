from typing import List
from aws_cdk import aws_eks as eks
from constructs import Construct
from .controller_plane import ControllerPlane
from .managed_node_group import EKSManagedNodeGroup
from .self_managed_node_group import SelfManagedNodeGroup
from .fargate_profile import FargateProfile


class EKSCluster(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        controller_plane: ControllerPlane,
        eks_managed_node_groups: List[EKSManagedNodeGroup] = [],
        self_managed_node_groups: List[SelfManagedNodeGroup] = [],
        fargate_profiles: List[FargateProfile] = [],
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)
        cluster = eks.Cluster(
            self,
            f"{controller_plane.cluster_name}",
            cluster_name=controller_plane.cluster_name,
            kubectl_lambda_role=controller_plane.kubectl_lambda_role,
            awscli_layer=controller_plane.awscli_layer,
            cluster_handler_environment=controller_plane.cluster_handler_environment,
            cluster_handler_security_group=controller_plane.cluster_handler_security_group,
            kubectl_environment=controller_plane.kubectl_environment,
            kubectl_layer=controller_plane.kubectl_layer,
            kubectl_memory=controller_plane.kubectl_memory,
            masters_role=controller_plane.masters_role,
            on_event_layer=controller_plane.on_event_layer,
            place_cluster_handler_in_vpc=controller_plane.place_cluster_handler_in_vpc,
            secrets_encryption_key=controller_plane.secrets_encryption_key,
            service_ipv4_cidr=controller_plane.service_ipv4_cidr,
            role=controller_plane.role,
            security_group=controller_plane.security_group,
            vpc=controller_plane.vpc,
            vpc_subnets=controller_plane.vpc_subnets,
            default_capacity=controller_plane.default_capacity,
            default_capacity_instance=controller_plane.default_capacity_instance,
            default_capacity_type=controller_plane.default_capacity_type,
            cluster_logging=controller_plane.cluster_logging,
            # dns compute type should be FARGATE when using fargate profile as data plane
            core_dns_compute_type=controller_plane.core_dns_compute_type,
            endpoint_access=controller_plane.endpoint_access,
            alb_controller=controller_plane.alb_controller,
            output_cluster_name=controller_plane.output_cluster_name,
            output_masters_role_arn=controller_plane.output_masters_role_arn,
            output_config_command=controller_plane.output_config_command,
            prune=controller_plane.prune,
            version=controller_plane.version,
        )
        for node_group in eks_managed_node_groups:
            cluster.add_auto_scaling_group_capacity(
                f"EKSASG{node_group.auto_scaling_group_name}",
                instance_type=node_group.instance_type,
                bootstrap_enabled=node_group.bootstrap_enabled,
                bootstrap_options=node_group.bootstrap_options,
                machine_image_type=node_group.machine_image_type,
                map_role=node_group.map_role,
                spot_interrupt_handler=node_group.spot_interrupt_handler,
                allow_all_outbound=node_group.allow_all_outbound,
                associate_public_ip_address=node_group.associate_public_ip_address,
                auto_scaling_group_name=node_group.auto_scaling_group_name,
                block_devices=node_group.block_devices,
                capacity_rebalance=node_group.capacity_rebalance,
                cooldown=node_group.cooldown,
                desired_capacity=node_group.desired_capacity,
                group_metrics=node_group.group_metrics,
                health_check=node_group.health_check,
                ignore_unmodified_size_properties=node_group.ignore_unmodified_size_properties,
                instance_monitoring=node_group.instance_monitoring,
                key_name=node_group.key_name,
                max_capacity=node_group.max_capacity,
                max_instance_lifetime=node_group.max_instance_lifetime,
                min_capacity=node_group.min_capacity,
                new_instances_protected_from_scale_in=node_group.new_instances_protected_from_scale_in,
                notifications=node_group.notifications,
                signals=node_group.signals,
                spot_price=node_group.spot_price,
                termination_policies=node_group.termination_policies,
                update_policy=node_group.update_policy,
                vpc_subnets=node_group.vpc_subnets,
            )
        for node_group in self_managed_node_groups:
            cluster.add_nodegroup_capacity(
                f"SELFEKSASG{node_group.nodegroup_name}",
                nodegroup_name=node_group.nodegroup_name,
                ami_type=node_group.ami_type,
                capacity_type=node_group.capacity_type,
                desired_size=node_group.desired_size,
                disk_size=node_group.disk_size,
                force_update=node_group.force_update,
                instance_types=node_group.instance_types,
                launch_template_spec=node_group.launch_template_spec,
                max_size=node_group.max_size,
                min_size=node_group.min_size,
                node_role=node_group.node_role,
                release_version=node_group.release_version,
                remote_access=node_group.remote_access,
                subnets=node_group.subnets,
                tags=node_group.tags,
                taints=node_group.taints,
            )

        for profile in fargate_profiles:
            cluster.add_fargate_profile(
                f"FARGATE{profile.fargate_profile_name}",
                selectors=profile.selectors,
                pod_execution_role=profile.pod_execution_role,
                subnet_selection=profile.subnet_selection,
                vpc=profile.vpc,
            )
