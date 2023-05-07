import pytest

pytestmark = pytest.mark.all_providers


resource_types = {
    "eks": "Custom::AWSCDK-EKS-Cluster",
    "ng": "AWS::EKS::Nodegroup",
    "asg": "AWS::AutoScaling::AutoScalingGroup",
    "fg": "Custom::AWSCDK-EKS-FargateProfile",
}


@pytest.fixture(scope="module")
def cdk_vars():
    return {
        "cluster_name": "SelfManagedNodeGroupEKS",
        "k8s_version": "1.24",
        "auto_scaling_group_name": "NodeGroupA",
        "min_capacity": 2,
        "nodegroup_name": "NodeGroupB",
        "desired_size": 2,
        "fargate_profile_name": "NodeGroupC",
    }


def test_resource(all_providers):
    for _, v in resource_types.items():
        all_providers.resource_count_is(v, 1)


def test_eks_cluster(all_providers, cdk_vars):
    all_providers.has_resource_properties(
        resource_types["eks"],
        {
            "Config": {
                "name": cdk_vars["cluster_name"],
                "version": cdk_vars["k8s_version"],
            }
        },
    )


def test_all_providers(all_providers, cdk_vars):
    all_providers.has_resource_properties(
        resource_types["asg"],
        {
            "AutoScalingGroupName": cdk_vars["auto_scaling_group_name"],
            "MinSize": str(cdk_vars["min_capacity"]),
        },
    )
    all_providers.has_resource_properties(
        resource_types["fg"],
        {"Config": {"selectors": [{"namespace": "app"}]}},
    )
    all_providers.has_resource_properties(
        resource_types["ng"],
        {
            "NodegroupName": cdk_vars["nodegroup_name"],
            "ScalingConfig": {"DesiredSize": cdk_vars["desired_size"]},
        },
    )
