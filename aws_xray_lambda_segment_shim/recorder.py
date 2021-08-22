import logging
import os
from typing import Dict

from aws_xray_sdk.core.context import Context
from aws_xray_sdk.core.models.segment import Segment
from aws_xray_sdk.core.models.trace_header import TraceHeader
from aws_xray_sdk.core.recorder import AWSXRayRecorder

from .segment import TriggeredSegmentContextManager

logger = logging.getLogger(__name__)


class TriggeredXrayRecorder(AWSXRayRecorder):
    """Provides setup defaults to allow trace continuation from any existing trace.

    Example:
        >>> from aws_xray_lambda_segment_shim import TriggeredXrayRecorder
        >>> from aws_xray_sdk.core.models.trace_header import TraceHeader
        >>> recorder = TriggeredXrayRecorder(
        ...     trace_header=TraceHeader(
        ...         root="1-5759e988-bd862e3fe1be46a994272793",
        ...         parent="3995c3f42cd8ad8",
        ...         sampled=1,
        ...     ),
        ...     trigger_metadata={"message_id": "059f36b4-87a3-44ab-83d2-661975830a7d"},
        ...     lambda_request_id="test_request_id",
        ...     lambda_arn="arn:aws:lambda:us-west-2:123456789012:function:my-function",
        ...     region="eu-west-1",
        ... )
        >>> with recorder.in_segment() as segment:
        ...     segment.trace_id
        '1-5759e988-bd862e3fe1be46a994272793'
    """

    def __init__(
        self,
        trace_header: TraceHeader,
        trigger_metadata: Dict[str, str],
        lambda_request_id: str,
        lambda_arn: str,
        region: str = None,
        setup_environment: bool = True,
    ) -> None:
        self.trace_header = trace_header
        self.trigger_metadata = trigger_metadata
        self.request_id = lambda_request_id
        self.lambda_arn = lambda_arn
        self.region = region or os.environ.get("AWS_REGION")
        self.setup_environment = setup_environment
        super().__init__()
        self._setup_triggered_recorder()

    def _setup_triggered_recorder(self) -> None:
        """Ensure we have a clean Context and not a LambdaContext.

        We also here set the aws metadata which get deepcopied into
        any newly created segment by the parent class.
        """
        self.configure(context=Context())

        self._aws_metadata = {
            **{
                "request_id": self.request_id,
                "operation": "SendMessage",
                "region": self.region,
            },
            **self.trigger_metadata,
        }

    def begin_segment(self, *args, **kwargs) -> Segment:
        """Begin the segment.

        Arguments:
            *args: Maintain for substitution compatibility with parent class, but ignored
            *kwargs: Maintain for substitution compatibility with parent class, but ignored
        """
        if args or kwargs:
            logger.warning(
                "Arguments passed erroneously to predefined segment, ignoring."
            )
        segment = self._setup_triggered_segment()
        if self.setup_environment:
            self._setup_triggered_xray_environment()
        return segment

    def _setup_triggered_segment(self) -> Segment:
        """Create the base segment."""
        segment = super().begin_segment(
            name=self.lambda_arn,
            traceid=self.trace_header.root,
            parent_id=self.trace_header.parent,
            sampling=self.trace_header.sampled,
        )
        segment.origin = "AWS::Lambda::Function"
        return segment

    def _setup_triggered_xray_environment(self) -> None:
        """Ensure boto3 and other patched libraries get instrumented with the correct trace id."""
        os.environ["_X_AMZN_TRACE_ID"] = self.trace_header.to_header_str()

    def in_segment(self) -> TriggeredSegmentContextManager:
        """Use as a context manager to autoclose the segment once left."""
        return TriggeredSegmentContextManager(self)
