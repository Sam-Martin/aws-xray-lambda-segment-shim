from typing import Union

from .entity import Entity

class Segment(Entity):
    origin: Union[None, str]
    id: Union[None, str]
