from projen.python import PythonProject, Setuptools
from projen.github import SemanticTitleOptions
from projen.github import GitHubOptions, PullRequestLintOptions
from projen.github import GithubWorkflow

semantic_options = SemanticTitleOptions(
    types=["feat", "fix", "chore", "docs", "test", "refactor", "build", "ci"]
)

pull_request_lint = PullRequestLintOptions(semantic_title_options=semantic_options)

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
    github_options=GitHubOptions(pull_request_lint_options=pull_request_lint),
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
