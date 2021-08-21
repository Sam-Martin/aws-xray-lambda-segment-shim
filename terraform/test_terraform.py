import argparse

import boto3
from aws_xray_sdk.core import patch, xray_recorder

patch(["boto3"])
xray_recorder.configure(sampling=True)

parser = argparse.ArgumentParser()
parser.add_argument("sqs_queue_url")
args = parser.parse_args()

with xray_recorder.in_segment("Test sqs-lambda-segment") as segment:
    sqs = boto3.client("sqs", region_name="eu-west-1")
    print(f"sending message to {args.sqs_queue_url} with trace id {segment.trace_id}")
    print(
        f"https://eu-west-1.console.aws.amazon.com/xray/home?region=eu-west-1#/traces/{segment.trace_id}"
    )
    sqs.send_message(QueueUrl=args.sqs_queue_url, MessageBody="{}")
