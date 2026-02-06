from color import Color
from display import display_board
from pawn import Pawn
from pawn_type import PawnType


def is_movement_allowed(board, mov, pawn: Pawn):
    type = pawn.get_type()

    if type == PawnType.PION:
        color = pawn.get_color()
        has_moved = pawn.get_has_moved()

        direction = 1 if color == Color.NOIR else -1
        coefficient = 2 * direction if not has_moved else direction

        print(mov)

        allowed_mov = type.value[2][0]

        print(allowed_mov[1] * coefficient)

        if ((allowed_mov[1] * coefficient <= 0 and 0 >= mov[1] >= allowed_mov[1] * coefficient) or (allowed_mov[1] * coefficient >= 0 and 0 <= mov[1] <= allowed_mov[1] * coefficient)) and mov[0] == allowed_mov[0]:
            return True
        
    if type == PawnType.ROI:
        if mov in type.value[2]:
            return True
    
    if type == PawnType.CAVALIER:
        if mov in type.value[2]:
            return True

    if type == PawnType.DAME:
        for allowed_mov in type.value[2]:
            if abs(mov[0]) <= abs(allowed_mov[0]) and abs(mov[1]) <= abs(allowed_mov[1]) and (abs(mov[0]) == 0 or abs(mov[1]) == 0 or abs(mov[0]) == abs(mov[1])):
                return True
    
    if type == PawnType.TOUR:
        for allowed_mov in type.value[2]:
            if abs(mov[0]) <= abs(allowed_mov[0]) and abs(mov[1]) <= abs(allowed_mov[1]):
                return True
    
    if type == PawnType.FOU:
        for allowed_mov in type.value[2]:
            if abs(mov[0]) <= abs(allowed_mov[0]) and abs(mov[1]) <= abs(allowed_mov[1]) and abs(mov[0]) == abs(mov[1]):
                return True

    return False

def play_round(board, player, round_count):
    display_board(board)

    print("---------------------------------")
    print(f"Au tour de {player.color}:")
    move = input("Entrez votre coup (ex: d4-e5): ")

    success = player.play(move)

    if not success:
        play_round(board, player, round_count)