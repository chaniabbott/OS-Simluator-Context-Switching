from enum import Enum, auto

class ProcessState(Enum):
    READY = auto()
    BLOCKED = auto()
    SUSPENDED_READY = auto()
    SUSPENDED_BLOCKED = auto()
    FINISHED = auto()