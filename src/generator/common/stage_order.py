from enum import Enum

class StageOrder(Enum):
    BEFORE_DEFAULT = -1
    DEFAULT = 0
    AFTER_DEFAULT = 1

    def __lt__(self, other):
        return self.value < other.value
