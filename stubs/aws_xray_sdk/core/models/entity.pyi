from inspect import Traceback
from traceback import StackSummary

class Entity:
    def add_exception(
        self, exception: Exception, stack: StackSummary, remote: bool = False
    ): ...
