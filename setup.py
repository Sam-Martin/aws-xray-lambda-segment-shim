#!/usr/bin/env python
"""Setup aws_xray_lambda_segment_shim package."""
import re
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = re.sub(r"..\s*doctest\s*::", ".. code-block ::", f.read())

setup(
    version="0.5.1",
    python_requires=">=3.6.0",
    name="aws_xray_lambda_segment_shim",
    packages=find_packages(include=["aws_xray_lambda_segment_shim"]),
    description="An unofficial shim which faciliates the creation of "
    "AWS Xray Segments in Lambda functions triggered by unsupported means.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Sam Martin",
    author_email="samjackmartin+aws-xray-lambda-segment-shim@gmail.com",
    url="https://github.com/sam-martin/aws-xray-lambda-segment-shim",
    install_requires=["aws-xray-sdk", "jmespath"],
    package_data={
        "": ["py.typed"],
    },
)
