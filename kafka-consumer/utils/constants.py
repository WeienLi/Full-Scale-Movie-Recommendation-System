from enum import Enum


class MessageType(Enum):
    """Enum for messages types"""

    RECOMMEND = "recommend"
    WATCHTIME = "watchtime"
    RATING = "rating"
    BROKEN = "broken"
