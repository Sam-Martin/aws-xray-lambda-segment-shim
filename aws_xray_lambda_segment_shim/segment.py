from typing import TYPE_CHECKING, Optional, Type

from aws_xray_sdk.core.models.segment import Segment

if TYPE_CHECKING:
    from .recorder import TriggeredXrayRecorder
else:
    TriggeredXrayRecorder = object
import traceback
from types import TracebackType


class TriggeredSegmentContextManager:
    """Wrapper for segment and recorder to provide segment context manager."""

    def __init__(self, recorder: TriggeredXrayRecorder) -> None:
        self.recorder = recorder
        self.segment: Optional[Segment] = None

    def __enter__(self) -> Segment:
        """Begin the segment when we enter the context."""
        self.segment = self.recorder.begin_segment()
        return self.segment

    def __exit__(
        self, exc_type: Type, exc_val: Exception, exc_tb: TracebackType
    ) -> None:
        """End the segment when we exit the context."""
        if self.segment is None:
            return

        if exc_type is not None:
            self.segment.add_exception(
                exc_val,
                traceback.extract_tb(
                    exc_tb,
                    limit=self.recorder.max_trace_back,
                ),
            )
        self.recorder.end_segment()
