from color import Color
from pawn import Pawn
from pawn_type import PawnType


def is_movement_allowed(board, mov, pawn: Pawn):
    type = pawn.get_type()

    if type == PawnType.PION:
        color = pawn.get_color()
        has_moved = pawn.get_has_moved()

        direction = 1 if color == Color.NOIR else -1
        coefficient = 2 * direction if not has_moved else direction

        allowed_mov = coefficient * type[2]

        if mov[0] <= allowed_mov[0] and mov[1] == 0:
            return True
        
    if type == PawnType.ROI:
        if mov in type[2]:
            return True
    
    if type == PawnType.CAVALIER:
        if mov in type[2]:
            return True

    if type == PawnType.DAME:
        for allowed_mov in type[2]:
            if abs(mov[0]) <= abs(allowed_mov[0]) and abs(mov[1]) <= abs(allowed_mov[1]):
                return True
    
    if type == PawnType.TOUR:
        for allowed_mov in type[2]:
            if abs(mov[0]) <= abs(allowed_mov[0]) and abs(mov[1]) <= abs(allowed_mov[1]):
                return True
    
    

    return False