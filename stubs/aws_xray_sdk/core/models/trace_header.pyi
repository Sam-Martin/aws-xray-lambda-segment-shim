from typing import Any, Dict, Union

class TraceHeader:
    root: Union[str, None]
    parent: Union[str, None]
    sampled: Union[bool, None]
    def __init__(
        self,
        root=Union[str, None],
        parent=Union[str, None],
        sampled=Union[int, None],
        data=Union[Dict[str, Any], None],
    ) -> None: ...
    @classmethod
    def from_header_str(cls, header: str) -> TraceHeader: ...
    def to_header_str(self) -> str: ...
