from enum import Enum

class Outcome(Enum):
    WIN = 0
    LOSS = 1
    PENDING = 3

class MatchTypes(Enum):
    CUSTOM_5V5 = 'RANKED_5V5'
    CUSTOM_1V1 = 'CUSTOM_1V1'