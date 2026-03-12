from color import Color
from display import display_board, display_points
from pawn import Pawn
from pawn_type import PawnType

def play_round(board, player, opponent, round_count):
    
    player.look_if_king_in_checkmate()

    if player.king_in_checkmate:
        print(f"Checkmate! {opponent.color.value} wins!")
        success = True
    else:
        display_board(board, player.king_attacked_moves)

        if player.color == Color.BLANC:
            display_points(player, opponent)
            print("Au tour de Blanc:")
        else:
            display_points(opponent, player)
            print("Au tour de Noir:")
        print("---------------------------------")
        move = input("Entrez votre coup (ex: d4-e5): ")
        success = player.play(move)

    if not success:
        play_round(board, player, opponent, round_count)


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

def is_king_in_check(board, color, king_attacked_moves : list):
    # Check if the king of the given color is in check
    king_position = King_position(board, color)
    if king_position is None:
        print("Error: King not found on the board")
        return False

     # The king is in check
    print("King position:", king_position)
    if king_position in king_attacked_moves:
        return True
    
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
    # Check if the path between the start and end positions is clear
    
    start_row, start_col = position

    if pawn.get_type() == PawnType.CAVALIER or pawn.get_type() == PawnType.PION:
        return True
    
    step_col = 0 if mov[0] == 0 else (1 if mov[0] > 0 else -1)
    step_row = 0 if mov[1] == 0 else (1 if mov[1] > 0 else -1)

    path = [(start_row + i * step_row, start_col + i * step_col) for i in range(1, max(abs(mov[0]), abs(mov[1])))]

    path_list = [board[row][col] for row, col in path if 0 <= row < 8 and 0 <= col < 8]

    print("Path:", path)
    print("Path list:", path_list)
    #Return True if all the squares in the path are empty (None)
    if all(piece is None for piece in path_list):
        print("Piece on the way")
    return all(piece is None for piece in path_list)



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
            if piece is not None and piece.get_color() != color and piece.get_type() != PawnType.ROI and piece.get_type() != PawnType.CAVALIER and piece.get_type() != PawnType.PION:
                for move in piece.get_type().value[2]:

                    start_row, start_col = row, col
                    
                    step_col = 0 if move[0] == 0 else (1 if move[0] > 0 else -1)
                    step_row = 0 if move[1] == 0 else (1 if move[1] > 0 else -1)

                    path = [(start_row + i * step_row, start_col + i * step_col) for i in range(1, max(abs(move[0]), abs(move[1])))]
                    path = [i for i in path if 0 <= i[0] < 8 and 0 <= i[1] < 8]
                    path_list = [board[row][col] for row, col in path if 0 <= row < 8 and 0 <= col < 8]

                    for i in range(len(path_list)):
                        if path_list[i] is not None:
                            path = path[:i + 1]
                            path_list = path_list[:i + 1]
                            break
                    for i in path:
                        if i not in attacked_moves:
                            attacked_moves.append(i)
            if piece is not None and piece.get_color() != color and (piece.get_type() == PawnType.ROI or piece.get_type() == PawnType.CAVALIER):
                for move in piece.get_type().value[2]:
                    new_row = row + move[1]
                    new_col = col + move[0]

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if (new_row, new_col) not in attacked_moves:
                            attacked_moves.append((new_row, new_col))
            if piece is not None and piece.get_color() != color and piece.get_type() == PawnType.PION:
                direction = 1 if piece.get_color() == Color.NOIR else -1
                for move in [(1, direction), (-1, direction)]:
                    new_row = row + move[1]
                    new_col = col + move[0]

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if (new_row, new_col) not in attacked_moves:
                            attacked_moves.append((new_row, new_col))         
    return attacked_moves

def King_castle_moves(board, color, direction):
    # Return a list of available castle moves for the king of the given color
    castle_moves = []

    king_position = King_position(board, color)
    if king_position is None:
        return castle_moves

    castle_moves = [(king_position[0], king_position[1] + i * direction) for i in range(1, 3)]
    
    return castle_moves

def every_piece_move(board, color):
    # Return a list of moves the player can make
    attacked_moves = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.get_color() == color and piece.get_type() != PawnType.ROI and piece.get_type() != PawnType.CAVALIER and piece.get_type() != PawnType.PION:
                for move in piece.get_type().value[2]:

                    start_row, start_col = row, col
                    
                    step_col = 0 if move[0] == 0 else (1 if move[0] > 0 else -1)
                    step_row = 0 if move[1] == 0 else (1 if move[1] > 0 else -1)

                    path = [(start_row + i * step_row, start_col + i * step_col) for i in range(1, max(abs(move[0]), abs(move[1])))]
                    path = [i for i in path if 0 <= i[0] < 8 and 0 <= i[1] < 8]
                    path_list = [board[row][col] for row, col in path if 0 <= row < 8 and 0 <= col < 8]

                    for i in range(len(path_list)):
                        if path_list[i] is not None:
                            path = path[:i + 1]
                            path_list = path_list[:i + 1]
                            break
                    for i in path:
                        if i not in attacked_moves:
                            attacked_moves.append(((row, col), i))
            if piece is not None and piece.get_color() == color and (piece.get_type() == PawnType.ROI or piece.get_type() == PawnType.CAVALIER):
                for move in piece.get_type().value[2]:
                    new_row = row + move[1]
                    new_col = col + move[0]

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if (new_row, new_col) not in attacked_moves:
                            attacked_moves.append(((row, col), (new_row, new_col)))
            if piece is not None and piece.get_color() == color and piece.get_type() == PawnType.PION:
                direction = 1 if piece.get_color() == Color.NOIR else -1
                for move in [(1, direction), (-1, direction)]:
                    new_row = row + move[1]
                    new_col = col + move[0]

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if (new_row, new_col) not in attacked_moves:
                            attacked_moves.append(((row, col), (new_row, new_col))) 
    return attacked_moves

def get_all_annotated_moves(board, color):
    # Look at all moves for all our pieces that are still in the 8x8 board using previouly build funtions

    valid_moves = []
    valid_moves = every_piece_move(board, color)

    #including pawn moves that are not attacks
    pawn_moves = [(0, 1), (0, 2), (1, 1), (-1, 1)] if color == Color.NOIR else [(0, -1), (0, -2), (1, -1), (-1, -1)]
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece.get_color() == color and piece.get_type() != PawnType.PION:
                for move in pawn_moves:

                    new_row = row + move[1]
                    new_col = col + move[0]

                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        valid_moves.append(((row, col), (new_row, new_col)))
    
    #Convert moves into chess notation
    chr_cte = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    num_cte = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
    notated_moves = [f"{chr_cte[i[0]]}{num_cte[i[1]]}-{chr_cte[j[0]]}{num_cte[j[1]]}" for i, j in valid_moves]

    return notated_moves