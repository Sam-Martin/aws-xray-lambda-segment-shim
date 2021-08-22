
TF_DATA_DIR=/tmp/.terraform-aws-xray-sqs-lambda-segment-shim
XRAY_DAEMON_URL=https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-macos-3.x.zip

terraform-init:
	mkdir -p ${TF_DATA_DIR}
	cd terraform && pip install aws-xray-sdk --target .
	rm -rf terraform/boto3 terraform/botocore
	cd terraform && TF_DATA_DIR=${TF_DATA_DIR} terraform init

terraform-apply:
	cd terraform && TF_DATA_DIR=${TF_DATA_DIR} terraform apply

terraform-destroy:
	cd terraform && TF_DATA_DIR=${TF_DATA_DIR} terraform destroy

terraform-send-message:
	QUEUE_URL=$$(cd terraform && terraform output --raw sqs_queue_url) && \
	python ./terraform/test_terraform.py $$QUEUE_URL

install-xray-daemon-mac:
	curl ${XRAY_DAEMON_URL} -o ~/Downloads/aws-xray-daemon-macos-3.x.zip
	unzip ~/Downloads/aws-xray-daemon-macos-3.x.zip -d xray_daemon

run-xray-daemon-mac:
	./xray_daemon/xray_mac -o -n eu-west-1

local-test:
	pytest
	mypy
	pydocstyle
	flake8
	isort aws_xray_sqs_lambda_segment_shim tests terraform/*.py


# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = doc_source
BUILDDIR      = doc_build
HTML_DIR      = docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD)  -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" -P $(SPHINXOPTS) $(O)
