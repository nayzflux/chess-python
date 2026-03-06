from color import Color
from display import display_board, display_points
from pawn import Pawn
from pawn_type import PawnType


def is_movement_allowed(board, mov, pawn: Pawn):
    type = pawn.get_type()

    if type == PawnType.PION:
        color = pawn.get_color()
        has_moved = pawn.get_has_moved()

        direction = 1 if color == Color.NOIR else -1
        # Standard one-square pawn move.
        if mov == (0, direction):
            return True

        # Initial two-square pawn move.
        if mov == (0, 2 * direction) and not has_moved:
            return True

        # Diagonal pawn move used for captures and en passant.
        if abs(mov[0]) == 1 and mov[1] == direction:
            return True
        
    if type == PawnType.ROI:
        # Check ROCK
        if (mov == (2, 0) or mov == (-2, 0)) and not pawn.get_has_moved():
            return True

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

def play_round(board, player, opponent, round_count):
    display_board(board)
    if player.color == Color.BLANC:
        display_points(player, opponent)
    else:
        display_points(opponent, player)

    print("---------------------------------")
    print(f"Au tour de {player.color}:")
    move = input("Entrez votre coup (ex: d4-e5): ")

    success = player.play(move)

    if not success:
        play_round(board, player, opponent, round_count)