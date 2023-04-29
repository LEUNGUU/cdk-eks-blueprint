from projen.python import PythonProject

project = PythonProject(
    author_email="liangy3928@gmail.com",
    author_name="leunguu",
    module_name="cdk_eks_blueprint",
    name="cdk-eks-blueprint",
    version="0.1.0",
)

project.synth()