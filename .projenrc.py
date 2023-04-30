from projen.python import PythonProject, Setuptools
from projen.release import Publisher, Release

project = PythonProject(
    author_email="liangy3928@gmail.com",
    author_name="leunguu",
    module_name="cdk_eks_blueprint",
    name="cdk-eks-blueprint",
    version="0.1.0",
    vscode=False,
    auto_approve_options={"allowed_usernames": ["leunguu"]},
    dev_deps=["pytest"],
)

package = Setuptools(
    project=project,
    author_email="liangy3928@gmail.com",
    author_name="leunguu",
    version="0.0.1",
)

publisher = Publisher(
    project=project,
    build_job_id="releasePypi",
    artifact_name="dist",
)

publisher.publish_to_py_pi()

project.synth()
