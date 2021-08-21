import json
import os
import sys

# sys.path.append(os.path.abspath("./"))
sys.path.append(os.path.abspath("./terraform"))

from aws_xray_sqs_lambda_segment_shim import SQSTriggeredXrayRecorder


def lambda_handler(event, context):
    print(json.dumps(event, default=str))
    for i, record in enumerate(event["Records"]):
        recorder = SQSTriggeredXrayRecorder(
            record=record,
            lambda_request_id=context.aws_request_id,
            lambda_arn=context.invoked_function_arn,
        )
        with recorder.in_subsegment(f"SQS Record {i}") as subsegment:
            print(
                "I'm triggered by an SQS Record and using trace id ",
                subsegment.trace_id,
            )
        recorder.end_segment()
