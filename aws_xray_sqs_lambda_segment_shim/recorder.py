import os
from typing import TYPE_CHECKING

import jmespath
from aws_xray_sdk.core.context import Context
from aws_xray_sdk.core.models.trace_header import TraceHeader
from aws_xray_sdk.core.recorder import AWSXRayRecorder

from .exceptions import ImmutableSegmentError

if TYPE_CHECKING:
    from aws_lambda_typing.events.sqs import SQSMessage
else:
    SQSMessage = {}


class SQSTriggeredXrayRecorder(AWSXRayRecorder):
    def __init__(
        self,
        record: SQSMessage,
        lambda_request_id: str,
        lambda_arn: str,
        region: str = None,
        setup_environment: bool = True,
    ) -> None:
        self.sqs_trace_header = TraceHeader.from_header_str(
            jmespath.search("attributes.AWSTraceHeader", record)
        )
        self.message_id = record.get("messageId")
        self.request_id = lambda_request_id
        self.lambda_arn = lambda_arn
        self.region = region or os.environ.get("AWS_REGION")
        super().__init__()
        self._setup_sqs_triggered_recorder()
        self._setup_sqs_triggered_segment()
        if setup_environment:
            self._setup_sqs_triggered_xray_environment()

    def _setup_sqs_triggered_recorder(self) -> None:
        """Ensure we have a clean Context and not a LambdaContext."""
        self.configure(context=Context())

        # Set recorder aws data
        self._aws_metadata = {
            "request_id": self.request_id,
            "operation": "SendMessage",
            "message_id": self.message_id,
            "region": self.region,
        }

    def _setup_sqs_triggered_segment(self):
        # Setup the base segment
        segment = super().begin_segment(
            name=self.lambda_arn,
            traceid=self.sqs_trace_header.root,
            parent_id=self.sqs_trace_header.parent,
            sampling=self.sqs_trace_header.sampled,
        )
        segment.origin = "AWS::Lambda::Function"

        self.trace_header = TraceHeader(
            root=self.sqs_trace_header.root,
            parent=segment.id,
            sampled=self.sqs_trace_header.sampled,
        )

    def _setup_sqs_triggered_xray_environment(self):
        # Ensure boto3 and other patched libraries get instrumented with the correct trace id.
        os.environ["_X_AMZN_TRACE_ID"] = self.trace_header.to_header_str()

    def begin_segment(self, name, traceid, parent_id, sampling):
        raise ImmutableSegmentError()

    def in_segment(self, name, **segment_kwargs):
        raise ImmutableSegmentError()
