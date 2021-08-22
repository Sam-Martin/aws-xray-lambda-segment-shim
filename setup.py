#!/usr/bin/env python
"""Setup aws_xray_sqs_lambda_segment_shim package."""
import re
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = re.sub(r"..\s*doctest\s*::", ".. code-block ::", f.read())

setup(
    version="0.4.1",
    python_requires=">=3.6.0",
    name="aws_xray_sqs_lambda_segment_shim",
    description="aws_xray_sqs_lambda_segment_shim is now called aws_xray_lambda_segment_shim.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Sam Martin",
    author_email="samjackmartin+aws-xray-sqsl-lambda-segment-shim@gmail.com",
    url="https://github.com/sam-martin/aws-xray-lambda-segment-shim",
    install_requires=["aws_xray_lambda_segment_shimh"],
    package_data={
        "": ["py.typed"],
    },
    classifiers=["Development Status :: 7 - Inactive"],
)
