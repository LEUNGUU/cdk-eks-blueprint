import pytest


pytestmark = pytest.mark.eks_managed_nodegroup

resource_types = {
    "asg": "AWS::AutoScaling::AutoScalingGroup",
    "eks": "Custom::AWSCDK-EKS-Cluster",
}


# This will be used by conftest.py
@pytest.fixture(scope="module")
def cdk_vars():
    return {
        "cluster_name": "ManagedNodeGroupEKS",
        "k8s_version": "1.24",
        "auto_scaling_group_name": "NodeGroupA",
        "min_capacity": 2,
    }


def test_resource(eks_managed_nodegroup):
    for _, v in resource_types.items():
        eks_managed_nodegroup.resource_count_is(v, 1)


def test_eks_cluster(eks_managed_nodegroup, cdk_vars):
    eks_managed_nodegroup.has_resource_properties(
        resource_types["eks"],
        {
            "Config": {
                "name": cdk_vars["cluster_name"],
                "version": cdk_vars["k8s_version"],
            }
        },
    )


def test_node_group(eks_managed_nodegroup, cdk_vars):
    eks_managed_nodegroup.has_resource_properties(
        resource_types["asg"],
        {
            "AutoScalingGroupName": cdk_vars["auto_scaling_group_name"],
            "MinSize": str(cdk_vars["min_capacity"]),
        },
    )
