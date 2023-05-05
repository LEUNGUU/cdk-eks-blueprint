from projen.python import PythonProject, Setuptools

project = PythonProject(
    author_email="liangy3928@gmail.com",
    author_name="leunguu",
    module_name="cdk_eks_blueprint",
    name="cdk-eks-blueprint",
    version="0.0.9",
    vscode=False,
    auto_approve_options={"allowed_usernames": ["leunguu"]},
    deps=[
        "semver",
        "aws-cdk.lambda-layer-kubectl-v24",
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
    ],
    dev_deps=["pytest", "black"],
)

project.gitignore.exclude("cdk.out/")

package = Setuptools(
    project=project,
    author_email="liangy3928@gmail.com",
    author_name="leunguu",
    version="0.0.9",
    setup_config={
        "install_requires": [
            "semver",
            "aws-cdk.lambda-layer-kubectl-v24",
            "aws-cdk-lib>=2.1.0, <3.0.0",
            "constructs>=10.0.5, <11.0.0",
        ]
    },
)

project.synth()
