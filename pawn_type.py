from enum import Enum

class PawnType(Enum):
    ROI = ("Roi", 0)
    DAME = ("Dame", 9)
    TOUR = ("Tour", 5)
    FOU = ("Fou", 3)
    CAVALIER = ("Cavalier", 3)
    PION = ("Pion", 1)