from typing import TYPE_CHECKING

import jmespath
from aws_xray_sdk.core.models.trace_header import TraceHeader

from .exceptions import InvalidMessageID, InvalidTraceHeader
from .recorder import SQSTriggeredXrayRecorder, TriggeredXrayRecorder

if TYPE_CHECKING:
    from aws_lambda_typing.events.sqs import SQSMessage
else:
    SQSMessage = {}


__all__ = ["SQSTriggeredXrayRecorder", "TriggeredXrayRecorder", "exceptions"]


def get_sqs_triggered_recorder(
    record: SQSMessage,
    lambda_request_id: str,
    lambda_arn: str,
    region: str = None,
    setup_environment: bool = True,
) -> TriggeredXrayRecorder:
    """Convert your SQS message record into a recorder."""
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
