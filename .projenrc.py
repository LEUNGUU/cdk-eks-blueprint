from projen.awscdk import AwsCdkPythonApp

project = AwsCdkPythonApp(
    author_email="liangy3928@gmail.com",
    author_name="Yuri Liang",
    cdk_version="2.1.0",
    module_name="cdk_eks_blueprint",
    name="cdk-eks-blueprint",
    version="0.1.0",
    dev_deps=["pytest@7.2.1", "black@23.1.0"],
)
project.gitignore.include("pyrightconfig.json")
project.gitignore.include(".env.sh")

project.synth()
