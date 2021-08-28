from typing import TYPE_CHECKING

import jmespath
from aws_xray_sdk.core.models.trace_header import TraceHeader

from .exceptions import InvalidMessageID, InvalidTraceHeader
from .recorder import TriggeredXrayRecorder

if TYPE_CHECKING:
    from aws_lambda_typing.events.sqs import SQSMessage
else:
    SQSMessage = dict


__all__ = ["TriggeredXrayRecorder", "exceptions"]


def get_sqs_triggered_recorder(
    record: SQSMessage,
    lambda_request_id: str,
    lambda_arn: str,
    region: str = None,
    setup_environment: bool = True,
) -> TriggeredXrayRecorder:
    """Continue a trace from an SQS message.

    For this to work the SQS message must have a trace header.
    Trace headers are populated in SQS messages when the message is put on the queue by
    an AWS X-Ray instrumented AWS SDK (e.g. boto3).

    For more on how SQS and X-Ray work
    `consult the documentation <https://docs.aws.amazon.com/xray/latest/devguide/xray-services-sqs.html>`__.

    example:
        >>> from aws_xray_lambda_segment_shim import get_sqs_triggered_recorder
        >>> # Setup the lambda handler
        >>> def lambda_handler(event, context):
        ...     for i, record in enumerate(event["Records"]):
        ...         recorder = get_sqs_triggered_recorder(
        ...             record=record,
        ...             lambda_request_id=context.aws_request_id,
        ...             lambda_arn=context.invoked_function_arn,
        ...         )
        ...         with recorder.in_segment() as segment:
        ...             print(
        ...                 "I'm triggered by an SQS Record and using trace id ",
        ...                 segment.trace_id
        ...             )
        >>> # Pretend we're invoking the lambda
        >>> lambda_handler(
        ...     event=MOCK_EVENT,
        ...     context=MOCK_CONTEXT,
        ... )
        I'm triggered by an SQS Record and using trace id  1-5759e988-bd862e3fe1be46a994272793

    """
    trace_header_str = jmespath.search("attributes.AWSTraceHeader", record)
    if not trace_header_str:
        raise InvalidTraceHeader("No trace header found in SQS record")
    trace_header = TraceHeader.from_header_str(trace_header_str)

    message_id = record.get("messageId")
    if not message_id:
        raise InvalidMessageID("No message id found in SQS Record")

    return TriggeredXrayRecorder(
        trace_header=trace_header,
        lambda_request_id=lambda_request_id,
        trigger_metadata={"message_id": message_id},
        lambda_arn=lambda_arn,
        setup_environment=setup_environment,
        region=region,
    )
