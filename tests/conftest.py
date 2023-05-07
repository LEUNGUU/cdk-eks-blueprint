import pytest
from aws_cdk import App
from aws_cdk.assertions import Template
from .scenarios.managed_nodegroup import ManagedNodeGroupEKS
from .scenarios.self_managed_nodegroup import SelfManagedNodeGroupEKS
from .scenarios.fargate_profile import ServerlessEKS
from .scenarios.all_providers import AllProviders


@pytest.fixture(scope="module")
def eks_managed_nodegroup(cdk_vars):
    app = App()
    managed_nodegroup_eks = ManagedNodeGroupEKS(
        app,
        cdk_vars["cluster_name"],
        cluster_name=cdk_vars["cluster_name"],
        k8s_version=cdk_vars["k8s_version"],
        auto_scaling_group_name=cdk_vars["auto_scaling_group_name"],
        min_capacity=cdk_vars["min_capacity"],
    )
    template = Template.from_stack(managed_nodegroup_eks)
    yield template


@pytest.fixture(scope="module")
def self_managed_nodegroup(cdk_vars):
    app = App()
    self_managed_nodegroup = SelfManagedNodeGroupEKS(
        app,
        cdk_vars["cluster_name"],
        cluster_name=cdk_vars["cluster_name"],
        k8s_version=cdk_vars["k8s_version"],
        nodegroup_name=cdk_vars["nodegroup_name"],
        desired_size=cdk_vars["desired_size"],
    )
    template = Template.from_stack(self_managed_nodegroup)
    yield template


@pytest.fixture(scope="module")
def fargate_profile(cdk_vars):
    app = App()
    fargate_profile = ServerlessEKS(
        app,
        cdk_vars["cluster_name"],
        cluster_name=cdk_vars["cluster_name"],
        k8s_version=cdk_vars["k8s_version"],
        fargate_profile_name=cdk_vars["fargate_profile_name"],
    )
    template = Template.from_stack(fargate_profile)
    yield template


@pytest.fixture(scope="module")
def all_providers(cdk_vars):
    app = App()
    all_providers = AllProviders(
        app,
        cdk_vars["cluster_name"],
        cluster_name=cdk_vars["cluster_name"],
        k8s_version=cdk_vars["k8s_version"],
        auto_scaling_group_name=cdk_vars["auto_scaling_group_name"],
        min_capacity=cdk_vars["min_capacity"],
        nodegroup_name=cdk_vars["nodegroup_name"],
        desired_size=cdk_vars["desired_size"],
        fargate_profile_name=cdk_vars["fargate_profile_name"],
    )
    template = Template.from_stack(all_providers)
    return template
