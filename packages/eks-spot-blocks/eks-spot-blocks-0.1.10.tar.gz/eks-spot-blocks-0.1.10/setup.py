import json
import setuptools

kwargs = json.loads("""
{
    "name": "eks-spot-blocks",
    "version": "0.1.10",
    "description": "eks spot blocks constructs for awscdk",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/eks-spot-blocks.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<hunhsieh@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/pahud/eks-spot-blocks.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "eks_spot_blocks",
        "eks_spot_blocks._jsii"
    ],
    "package_data": {
        "eks_spot_blocks._jsii": [
            "eks-spot-blocks@0.1.10.jsii.tgz"
        ],
        "eks_spot_blocks": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.5.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-ec2>=1.44.0, <2.0.0",
        "aws-cdk.aws-eks>=1.44.0, <2.0.0",
        "aws-cdk.aws-iam>=1.44.0, <2.0.0",
        "aws-cdk.aws-ssm>=1.44.0, <2.0.0",
        "aws-cdk.core>=1.44.0, <2.0.0",
        "constructs>=3.0.3, <4.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
