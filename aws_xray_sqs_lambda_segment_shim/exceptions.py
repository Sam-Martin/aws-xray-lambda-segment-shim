class ImmutableSegmentError(Exception):
    """Thrown to avoid confusion as the segment is created in __init__ of SQSTriggeredXrayRecorder."""

    def __init__(self) -> None:
        super().__init__("SQSTriggeredXrayRecorder have immutable segments")
