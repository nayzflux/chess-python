

from color import Color
from pawn import Pawn
from pawn_type import PawnType


def init_board():
    board = [
        [Pawn(PawnType.TOUR, Color.NOIR), Pawn(PawnType.CAVALIER, Color.NOIR), Pawn(PawnType.FOU, Color.NOIR), Pawn(PawnType.DAME, Color.NOIR), Pawn(PawnType.ROI, Color.NOIR), Pawn(PawnType.FOU, Color.NOIR), Pawn(PawnType.CAVALIER, Color.NOIR), Pawn(PawnType.TOUR, Color.NOIR)],
        [Pawn(PawnType.PION, Color.NOIR) for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [Pawn(PawnType.PION, Color.NOIR) for _ in range(8)],
        [Pawn(PawnType.TOUR, Color.BLANC), Pawn(PawnType.CAVALIER, Color.BLANC), Pawn(PawnType.FOU, Color.BLANC), Pawn(PawnType.DAME, Color.BLANC), Pawn(PawnType.ROI, Color.BLANC), Pawn(PawnType.FOU, Color.BLANC), Pawn(PawnType.CAVALIER, Color.BLANC), Pawn(PawnType.TOUR, Color.BLANC)],
    ]