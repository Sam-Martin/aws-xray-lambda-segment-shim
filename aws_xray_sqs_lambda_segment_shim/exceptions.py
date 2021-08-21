class ImmutableSegmentError(Exception):
    def __init__(self) -> None:
        super().__init__("SQSTriggeredXrayRecorder have immutable segments")
