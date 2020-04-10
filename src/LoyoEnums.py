from enum import Enum

class Outcome(Enum):
    WIN = 'WIN'
    LOSS = 'LOSS'
    PENDING = 'PENDING'

class MatchTypes(Enum):
    CUSTOM_5V5 = 'RANKED_5V5'
    CUSTOM_1V1 = 'CUSTOM_1V1'