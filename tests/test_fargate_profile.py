import pytest

pytestmark = pytest.mark.fargate_profile

resource_types = {
    "asg": "Custom::AWSCDK-EKS-FargateProfile",
    "eks": "Custom::AWSCDK-EKS-Cluster",
}


@pytest.fixture(scope="module")
def cdk_vars():
    return {
        "cluster_name": "FargateProfileEKS",
        "k8s_version": "1.24",
        "fargate_profile_name": "NodeGroupC",
    }


def test_resource(fargate_profile):
    fargate_profile.resource_count_is(resource_types["eks"], 1)
    fargate_profile.resource_count_is(resource_types["asg"], 1)


def test_eks_cluster(fargate_profile, cdk_vars):
    fargate_profile.has_resource_properties(
        resource_types["eks"],
        {
            "Config": {
                "name": cdk_vars["cluster_name"],
                "version": cdk_vars["k8s_version"],
            }
        },
    )


def test_node_group(fargate_profile):
    fargate_profile.has_resource_properties(
        resource_types["asg"],
        {
            "Config": {
                "selectors": [{"namespace": "kube-system"}, {"namespace": "default"}]
            }
        },
    )
