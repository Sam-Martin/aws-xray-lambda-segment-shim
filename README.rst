aws-xray-sqs-lambda-segment-shim
=====================================

|shield1| |shield2|

.. |shield1| image:: https://img.shields.io/github/workflow/status/sam-martin/aws-xray-sqs-lambda-segment-shim/Linting%20&%20Testing?style=flat-square
    :target: https://github.com/Sam-Martin/aws-xray-sqs-lambda-segment-shim/actions/workflows/continuous-integration.yml?query=branch%3Amain+
    :alt: GitHub Workflow Status

.. |shield2|  image:: https://img.shields.io/pypi/v/aws-xray-sqs-lambda-segment-shim?style=flat-square
    :target: https://pypi.org/project/aws-xray-sqs-lambda-segment-shim/
    :alt: PyPI

.. image:: https://github.com/Sam-Martin/aws-xray-sqs-lambda-segment-shim/blob/main/images/example.png?raw=true

It's not currently possibly follow an AWS Xray trace through a Lambda Function triggered by an SQS Queue.

Unless you use ``aws-xray-sqs-lambda-segment-shim``!

Installation
----------------

.. code-block::

    pip install aws-xray-sqs-lambda-segment-shim


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


Caveats
----------

This approach causes all subsegments created with it to appear only in the trace that was passed in by SQS.
There will still be a separate Lambda trace that will not contain these subsegments and will not show as
being triggered by SQS.

This approach is useful if you are using SQS as an intermediary for a process you're already tracing as it
then makes logical sense to view the traces from that starting point.

If you're more likely to view your traces as starting at the lambda function
(i.e. you do **not** have any tracing prior to the SQS queue) then your mileage may vary with this approach.

We are also here working outside the scope of what is expected by the aws-xray-sdk.
We are pretending to be AWS Lambda when we're initiating a trace, we're using undocumented fields to
pretend to be AWS Lambda, and to allow the correlation of the SQS message and the Lambda Invocation (edge creation).

If this wasn't the only way to pursue a trace through SQS to lambda I would suggest you avoid it! But given the
complexity involved in automating this from AWS's side, it may be a while before we see native support.

- `Issue on Python SDK <https://github.com/aws/aws-xray-sdk-python/issues/173>`__
- `Issue on .NET SDK <https://github.com/aws/aws-xray-sdk-dotnet/issues/110>`__
- `Issue on Node SDK <https://github.com/aws/aws-xray-sdk-node/issues/208>`__
