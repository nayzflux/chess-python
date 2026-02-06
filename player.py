import re
from pawn import Pawn
import game

board_square = {
    # Files
    "a": 7, "b": 6, "c": 5, "d": 4, "e": 3, "f": 2, "g": 1, "h": 0,
    "A": 7, "B": 6, "C": 5, "D": 4, "E": 3, "F": 2, "G": 1, "H": 0,

    # Lines
    "1": 0, "2": 1, "3": 2, "4": 3,"5": 4, "6": 5, "7": 6, "8": 7
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
            return

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
            return
        
        if isinstance(start_pawn, Pawn) and start_pawn.get_color() != self.color:
            print("This is not your piece, you can only play your pieces")
            return
        
        mov = (end_col - start_col, end_row - start_row)

        if not game.is_movement_allowed(self.board, mov, start_pawn):
            print("Move not allowed for this piece")
            return
        
        print("Valid chess move")

        # Move the piece










