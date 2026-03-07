from color import Color
from display import display_board, display_points
from pawn import Pawn
from pawn_type import PawnType


def is_movement_allowed(board, mov, pawn: Pawn, position):
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
                print(mov)
                if is_path_clear(board, mov, position, pawn):
                    return True
        return False
    
    if type == PawnType.TOUR:
        for allowed_mov in type.value[2]:
            if abs(mov[0]) <= abs(allowed_mov[0]) and abs(mov[1]) <= abs(allowed_mov[1]):
                print(mov)
                if is_path_clear(board, mov, position, pawn):
                    return True
        return False
    
    if type == PawnType.FOU:
        for allowed_mov in type.value[2]:
            if abs(mov[0]) <= abs(allowed_mov[0]) and abs(mov[1]) <= abs(allowed_mov[1]) and abs(mov[0]) == abs(mov[1]):
                print(mov)
                if is_path_clear(board, mov, position, pawn):
                    return True
        return False

    return False


def King_position(board, color):
    # Return the position of the king of the given color
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.get_type() == PawnType.ROI and piece.get_color() == color:
                return (row, col)
    return None

def is_king_in_check(board, pawn, color, king_attacked_moves : list):
    # Check if the king of the given color is in check
    king_position = King_position(board, color)
    if king_position is None:
        return False

     # The king has is in check
    if king_position in king_attacked_moves:
        return False 
    
def is_king_in_checkmate(board, pawn, color, king_attacked_moves : list, king_available_moves : list):
    # Check if the king of the given color is in checkmate
    if not is_king_in_check(board, pawn, color, king_attacked_moves):
        return False

    # Check if the king has any legal move to escape check
    for move in king_available_moves:
        if move not in king_attacked_moves:
            return False

    return True


def is_path_clear(board, mov, position, pawn):
    # Vérifie si le chemin entre start et end est dégagé
    
    start_row, start_col = position

    if pawn.get_type() == PawnType.CAVALIER or pawn.get_type() == PawnType.PION:
        return True
    
    step_col = 0 if mov[0] == 0 else (1 if mov[0] > 0 else -1)
    step_row = 0 if mov[1] == 0 else (1 if mov[1] > 0 else -1)

    path = [(start_row + i * step_row, start_col + i * step_col) for i in range(1, max(abs(mov[0]), abs(mov[1])))]

    path_list = [board[row][col] for row, col in path]

    print("Path:", path)
    print("Path list:", path_list)
    #Return True if all the squares in the path are empty (None)
    if all(piece is None for piece in path_list):
        print("Piece on the way")
    return all(piece is None for piece in path_list)


def play_round(board, player, opponent, round_count):
    display_board(board)
    if player.color == Color.BLANC:
        display_points(player, opponent)
        print(f"Au tour de Blanc:")
    else:
        display_points(opponent, player)
        print(f"Au tour de Noir:")

    print("---------------------------------")
    move = input("Entrez votre coup (ex: d4-e5): ")

    success = player.play(move)

    if not success:
        play_round(board, player, opponent, round_count)


def King_available_moves(board, color, king_attacked_moves : list):
    # Return a list of available moves for the king at the given position
    available_moves = []

    king_position = King_position(board, color)
    if king_position is None:
        return available_moves
    for move in PawnType.ROI.value[2]:
        new_row = king_position[0] + move[1]
        new_col = king_position[1] + move[0]

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] is None and (new_row, new_col) not in king_attacked_moves:
                available_moves.append((new_row, new_col))
            elif board[new_row][new_col] is not None and board[new_row][new_col].get_color() != color and (new_row, new_col) not in king_attacked_moves:
                available_moves.append((new_row, new_col))
    return available_moves


def King_attacked_moves(board, color):
    # Return a list of moves that attack the king of the given color
    attacked_moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.get_color() != color:
                for move in piece.get_type().value[2]:
                    new_row = row + move[1]
                    new_col = col + move[0]

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        attacked_moves.append((new_row, new_col))
    
    return attacked_moves