import time
from typing import Optional, Union

from aws_xray_sdk.core.context import Context
from aws_xray_sdk.core.emitters.udp_emitter import UDPEmitter
from aws_xray_sdk.core.models.default_dynamic_naming import DefaultDynamicNaming
from aws_xray_sdk.core.models.segment import Segment
from aws_xray_sdk.core.sampling.sampler import DefaultSampler, LocalSampler
from aws_xray_sdk.core.streaming.default_streaming import DefaultStreaming

class AWSXRayRecorder:
    def __init__(self) -> None: ...
    def configure(
        self,
        sampling: Union[bool, None] = None,
        plugins: Union[set, None] = None,
        context_missing: Union[str, None] = None,
        sampling_rules: Union[set, None] = None,
        daemon_address: Union[str, None] = None,
        service: Union[str, None] = None,
        context: Union[Context, None] = None,
        emitter: Union[UDPEmitter, None] = None,
        streaming: Union[DefaultStreaming, None] = None,
        dynamic_naming: Union[DefaultDynamicNaming, None] = None,
        streaming_threshold: Union[int, None] = None,
        max_trace_back: Union[int, None] = None,
        sampler: Union[LocalSampler, DefaultSampler, None] = None,
        stream_sql=Union[bool, None],
    ): ...
    def begin_segment(
        self,
        name: Union[str, None],
        traceid: Union[str, None],
        parent_id: Union[str, None],
        sampling: Union[bool, None],
    ) -> Segment: ...
    def end_segment(self, end_time: Optional[time.struct_time] = None): ...
    @property
    def max_trace_back(self) -> int: ...
