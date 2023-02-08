from enum import Enum

class EventType(int, Enum):
    CONF_FORUM = 1
    MEETING = 2
    TA = 3
    TRAINING = 4
    OTHER = 99