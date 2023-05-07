import pytest

pytestmark = pytest.mark.self_managed_nodegroup


resource_types = {"asg": "AWS::EKS::Nodegroup", "eks": "Custom::AWSCDK-EKS-Cluster"}


# This will be used by conftest.py
@pytest.fixture(scope="module")
def cdk_vars():
    return {
        "cluster_name": "SelfManagedNodeGroupEKS",
        "k8s_version": "1.24",
        "nodegroup_name": "NodeGroupB",
        "desired_size": 2,
    }


def test_resource(self_managed_nodegroup):
    self_managed_nodegroup.resource_count_is(resource_types["eks"], 1)
    self_managed_nodegroup.resource_count_is(resource_types["asg"], 1)


def test_eks_cluster(self_managed_nodegroup, cdk_vars):
    self_managed_nodegroup.has_resource_properties(
        resource_types["eks"],
        {
            "Config": {
                "name": cdk_vars["cluster_name"],
                "version": cdk_vars["k8s_version"],
            }
        },
    )


def test_node_group(self_managed_nodegroup, cdk_vars):
    self_managed_nodegroup.has_resource_properties(
        resource_types["asg"],
        {
            "NodegroupName": cdk_vars["nodegroup_name"],
            "ScalingConfig": {"DesiredSize": cdk_vars["desired_size"]},
        },
    )
