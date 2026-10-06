from enum import Enum, auto

#These are all my states
class ProcessState(Enum):
    READY = auto()
    BLOCKED = auto()
    SUSPENDED_READY = auto()
    SUSPENDED_BLOCKED = auto()
    FINISHED = auto()