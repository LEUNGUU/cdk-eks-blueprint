import os
from aws_cdk import App, Environment
from cdk_eks_blueprint.main import MyStack

# for development, use account/region from cdk cli
dev_env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)

app = App()
MyStack(app, "testeks", "testeks", env=dev_env)

app.synth()
