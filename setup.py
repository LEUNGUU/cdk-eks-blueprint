# ~~ Generated by projen. To modify, edit .projenrc.py and run "npx projen".

import json
from setuptools import setup

kwargs = json.loads(
    """
{
    "name": "cdk-eks-blueprint",
    "python_requires": ">=3.7",
    "author": "leunguu",
    "author_email": "liangy3928@gmail.com",
    "version": "0.0.7",
    "install_requires": [
        "semver",
        "aws-cdk.lambda-layer-kubectl-v24",
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0"
    ]
}
"""
)

setup(**kwargs)
