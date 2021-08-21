
TF_DATA_DIR=/tmp/.terraform-aws-xray-sqs-lambda-segment-shim
XRAY_DAEMON_URL=https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-macos-3.x.zip

terraform-init:
	cd terraform && pip install aws-xray-sdk --target .
	cd terraform && TF_DATA_DIR=${TF_DATA_DIR} terraform init

terraform-apply:
	cd terraform && TF_DATA_DIR=${TF_DATA_DIR} terraform apply

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
