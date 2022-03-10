from enum import Enum

class StrategyStage(Enum):
    MACROS = 0
    HEADER_AND_STRUCTURE = 1
    PARAMS = 2
    OUTPUTS = 3
    COMMAND = 4
    TESTS = 5
    HELP = 6
    CITATIONS = 7

    def __lt__(self, other):
        return self.value < other.value
