import os
from aws_cdk import App, Environment
from tests.eks_stack import Captain

# for development, use account/region from cdk cli
dev_env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)

app = App()
Captain(app, "captain", "captain", env=dev_env)

app.synth()
