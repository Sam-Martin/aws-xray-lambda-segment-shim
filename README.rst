aws-xray-sqs-lambda-segment-shim
=====================================

.. image: https://raw.githubusercontent.com/Sam-Martin/aws-xray-sqs-lambda-segment-shim/main/images/example.png

It's not currently possibly follow an AWS Xray trace through a Lambda Function triggered by an SQS Queue.

Unless you use ``aws-xray-sqs-lambda-segment-shim``!

Installation
----------------

.. code-block::

    pip install aws-xray-lambda-segment-shim


Usage
------

.. doctest::

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

``SQSTriggeredXrayRecorder`` is a child class of ``aws_xray_sdk.AWSXRayRecorder`` so you can use all the methods you would expect
from following the `aws-xray-sdk documentation <https://github.com/aws/aws-xray-sdk-python/>`__.
