import re
from pawn import Pawn
import game
from pawn_type import PawnType

board_square = {
    # Files
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7,
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,

    # Lines
    "1": 7, "2": 6, "3": 5, "4": 4,"5": 3, "6": 2, "7": 1, "8": 0
}

class Player:
    def __init__(self, board, color):
        self.has_win = False
        self.color = color
        self.king_in_check = False
        self.board = board
        self.taken_pieces = []
        self.points = 0


    def play(self, move : str):
        pattern = r"[a-hA-H][1-8]-[a-hA-H][1-8]"
        move = move.strip()

        if not re.fullmatch(pattern, move):
            print("Invalid format, please use the format 'a2-a3' or 'A2-A3'")
            return False

        print("Valid move format")
        
        # Convert move string to coordinates
        start_col = board_square[move[0]]
        start_row = board_square[move[1]]
        end_col = board_square[move[3]]
        end_row = board_square[move[4]]

        start_pawn = self.board[start_row][start_col]
        end_pawn = self.board[end_row][end_col]

        if start_pawn is None:
            print("No piece at starting position")
            return False
        
        # Check if the piece belongs to the player
        if isinstance(start_pawn, Pawn) and start_pawn.get_color() != self.color:
            print("This is not your piece, you can only play your pieces")
            return False
        
        mov = (end_col - start_col, end_row - start_row)

        if not game.is_movement_allowed(self.board, mov, start_pawn):
            print("Move not allowed for this piece")
            return False
        
        # Check for piece at the final destination
        if end_pawn is not None and end_pawn.color == self.color:
            print("You cannot take your own piece")
            return False
        
        # Detect if the move is ROCK
        is_rock = False
        is_big_rock = False

        if start_pawn.get_type() == PawnType.ROI and abs(end_col - start_col) == 2 and not start_pawn.has_moved:
            is_rock = True
            if end_col - start_col == -2:
                is_big_rock = True
                print("Big ROCK detected")
            else:
                print("Small ROCK detected")

        # Check if rock is valid
        if is_rock:
            tower_col = 0 if is_big_rock else 7
            tower = self.board[start_row][tower_col]

            # Check if tower has moved
            if tower is None or tower.get_type() != PawnType.TOUR or tower.get_color() != self.color or tower.get_has_moved():
                print("ROCK not allowed because the tower is not valid")
                return False

            # Check if piece on the way for ROCK (Tower and King)
            direction = -1 if is_big_rock else 1

            for col in range(start_col + direction, tower_col, direction):
                if self.board[start_row][col] is not None:
                    print("ROCK not allowed because there is a piece between the king and the tower")
                    return False

        # TODO: Check for piece in the way
        
        # TODO: Check for danger on King

        # TODO: Check if danger on the way for ROCK (Tower and King)
        
        print("Valid chess move")
        
        # Take opponent piece if there is one
        if not is_rock and end_pawn is not None and end_pawn.color != self.color:
            print("You take an opponent piece")
            self.take(end_pawn)

        # Move the tower for ROCK
        if is_rock:
            tower_col = 0 if is_big_rock else 7
            new_tower_col = start_col + (-1 if is_big_rock else 1)

            self.board[start_row][new_tower_col] = self.board[start_row][tower_col]
            self.board[start_row][tower_col] = None
            self.board[start_row][new_tower_col].set_has_moved(True)

        # Move the piece
        start_pawn.set_has_moved(True)

        self.board[end_row][end_col] = start_pawn
        self.board[start_row][start_col] = None

        return True
    
    def take(self, taken_piece: Pawn):
        # Add points for taken piece
        self.points += taken_piece.get_points()

        # Add taken piece to the list of taken pieces
        self.taken_pieces.append(taken_piece)

        # Remove taken piece from board
        for row in self.board:
            for i in range(len(row)):
                if row[i] == taken_piece:
                    row[i] = None