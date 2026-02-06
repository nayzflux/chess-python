import re
from pawn import Pawn
import game

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


    def play(self, move : str):
        pattern = r"[a-hA-H][1-8]-[a-hA-H][1-8]"
        move = move.strip()

        if not re.fullmatch(pattern, move):
            print("Invalid format, please use the format 'a2-a3' or 'A2-A3'")
            return False

        print("Valid move format")
        
        # Convertir la notation en indices
        start_col = board_square[move[0]]
        start_row = board_square[move[1]]
        end_col = board_square[move[3]]
        end_row = board_square[move[4]]

        start_pawn = self.board[start_row][start_col]
        end_pawn = self.board[end_row][end_col]

        if start_pawn is None:
            print("No piece at starting position")
            return False
        
        if isinstance(start_pawn, Pawn) and start_pawn.get_color() != self.color:
            print("This is not your piece, you can only play your pieces")
            return False
        
        mov = (end_col - start_col, end_row - start_row)

        if not game.is_movement_allowed(self.board, mov, start_pawn):
            print("Move not allowed for this piece")
            return False
        
        # Check for piece in the way
        if end_pawn.color == self.color:
            # TODO: ROCK handle
            print("You cannot take your own piece")
            return False
        
        print("Valid chess move")
        
        # Take opponent piece if there is one
        if end_pawn is not None and end_pawn.color != self.color:
            print("You take an opponent piece")
            # TODO: Handle piece taking (remove from board, add to taken pieces list, add points)

        # Move the piece
        start_pawn.set_has_moved(True)

        self.board[end_row][end_col] = start_pawn
        self.board[start_row][start_col] = None

        return True









