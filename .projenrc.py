from projen.awscdk import AwsCdkPythonApp

project = AwsCdkPythonApp(
    author_email="yurliang@amazon.com",
    author_name="Yuri Liang",
    cdk_version="2.1.0",
    module_name="cdk_eks_blueprint",
    name="cdk-eks-blueprint",
    version="0.1.0",
    devDeps=["pytest"]
)

project.synth()
