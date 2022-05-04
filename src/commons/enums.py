from enum import Enum


class BOT_MODES(Enum):
    # Remote control mode
    rc = 0
    # Hide and Seek (autonomous)
    hide_and_seek = 1
    # Follow any cat or dog it sees (autonomous)
    follow = 2


VALID_BOT_MODES = set(item.value for item in BOT_MODES)
