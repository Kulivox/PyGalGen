from enum import Enum

class StageOrder(Enum):
    BEFORE_DEFAULT = -1
    OVERRIDE_DEFAULT = 0
    AFTER_DEFAULT = 1
