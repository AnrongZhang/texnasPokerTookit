from enum import Enum
from dataclasses import dataclass


class PatternFace(Enum):
    EMPTY = 0
    AHIGH = 1
    OPAIR = 2
    TPAIR = 3
    THREE = 4
    STRAI = 5
    FLUSH = 6
    FULLH = 7
    FOURK = 8
    SRIFL = 9

@dataclass
class Pattern:
    pattern_face: PatternFace = PatternFace.EMPTY
    pattern_weight: int = 0
