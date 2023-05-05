from aws_cdk.assertions import Capture, Match, Template
from aws_cdk import App
from .eks_stack import Captain


def test_synthesizes_properly():
    app = App()

    # create captain stack
    captain = Captain(app, "Captain", "Captain")

    # Prepare stack for assertions
    template = Template.from_stack(captain)

    template.has_resource_properties(
        "Custom::AWSCDK-EKS-Cluster", {"Config": {"version": "1.24", "name": "Captain"}}
    )

    template.has_resource_properties(
        "AWS::AutoScaling::AutoScalingGroup", {"AutoScalingGroupName": "apple"}
    )
    template.has_resource_properties("AWS::EKS::Nodegroup", {"NodegroupName": "banana"})
    template.has_resource_properties(
        "Custom::AWSCDK-EKS-FargateProfile",
        {"Config": {"selectors": [{"namespace": "app"}]}},
    )
