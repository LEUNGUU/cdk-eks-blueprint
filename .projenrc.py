from projen.python import PythonProject, Setuptools
from projen.release import Publisher, Release

project = PythonProject(
    author_email="liangy3928@gmail.com",
    author_name="leunguu",
    module_name="cdk_eks_blueprint",
    name="cdk-eks-blueprint",
    version="0.0.7",
    vscode=False,
    auto_approve_options={"allowed_usernames": ["leunguu"]},
    deps=[
        "semver@3.0.0-dev.4",
        "aws-cdk.lambda-layer-kubectl-v24",
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
    ],
    dev_deps=["pytest"],
)

package = Setuptools(
    project=project,
    author_email="liangy3928@gmail.com",
    author_name="leunguu",
    version="0.0.7",
    setup_config={
        "install_requires": [
            "semver",
            "aws-cdk.lambda-layer-kubectl-v24",
            "aws-cdk-lib>=2.1.0, <3.0.0",
            "constructs>=10.0.5, <11.0.0",
        ]
    },
)

publisher = Publisher(
    project=project,
    build_job_id="releasePypi",
    artifact_name="dist",
)

publisher.publish_to_py_pi()

project.synth()
