from typing import Any, Dict, Union

class TraceHeader:
    def __init__(
        self,
        root=Union[str, None],
        parent=Union[str, None],
        sampled=Union[int, None],
        data=Union[Dict[str, Any], None],
    ) -> None: ...
    @classmethod
    def from_header_str(cls, header: str) -> None: ...
