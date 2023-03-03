from enum import Enum


class BEHAVIORS(Enum):
    # Remote control mode
    RC = 0
    # Follow any person, cat or dog it sees (autonomous)
    FOLLOW = 1


VALID_BEHAVIORS = set(item.value for item in BEHAVIORS)
DEFAULT_BEHAVIOR = BEHAVIORS.RC
