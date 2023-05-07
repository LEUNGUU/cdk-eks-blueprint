import os
from aws_cdk import App, Environment
from tests.scenarios.fargate_profile import ServerlessEKS

# for development, use account/region from cdk cli
dev_env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)

cdk_vars = {
    "cluster_name": "FargateProfileEKS",
    "k8s_version": "1.24",
    "fargate_profile_name": "NodeGroupC",
}
app = App()
fargate_profile = ServerlessEKS(
    app,
    cdk_vars["cluster_name"],
    cluster_name=cdk_vars["cluster_name"],
    k8s_version=cdk_vars["k8s_version"],
    fargate_profile_name=cdk_vars["fargate_profile_name"],
)
app.synth()
