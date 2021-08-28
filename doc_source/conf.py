import os
import sys

import sphinx_rtd_theme  # noqa

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "aws-xray-lambda-segment-shim "
copyright = "2021, Sam Martin"
author = "Sam Martin"

# The full version, including alpha/beta/rc tags
release = "0.0.0"

nitpicky = True


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autodoc.typehints",
    "sphinx.ext.doctest",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- intersphinx
intersphinx_mapping = {
    "aws_xray_sdk": (
        "https://docs.aws.amazon.com/xray-sdk-for-python/latest/reference/",
        None,
    ),
}

# -- Napoleon
napoleon_include_init_with_doc = True

# -- Autodoc
add_module_names = False
autodoc_typehints = "description"


# -- Doctest
doctest_global_setup = """
from unittest.mock import Mock
MOCK_CONTEXT = Mock(
    aws_request_id="test-request",
    invoked_function_arn="arn:aws:lambda:us-west-2:123456789012:function:my-function"
)
MOCK_EVENT = {
    "Records": [
        {
            "attributes": {
                "AWSTraceHeader": "Root=1-5759e988-bd862e3fe1be46a994272793;Parent=3995c3f42cd8ad8;Sampled=1"
            },
            "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
        }
    ]
}
"""
