from color import Color
import re
from pawn import Pawn
import game
from pawn_type import PawnType
import copy

board_square = {
    # Files
    "a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7,
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,

    # Lines
    "1": 7, "2": 6, "3": 5, "4": 4,"5": 3, "6": 2, "7": 1, "8": 0
}

class Player:
    def __init__(self, board, color: Color):
        self.en_passant_target: Pawn | None = None
        self.has_rock = False
        self.has_win = False
        self.color = color
        self.king_in_check = False
        self.king_in_checkmate = False
        self.in_stalemate = False
        self.board = board
        self.taken_pieces = []
        self.points = 0
        self.simulation_board = []
        self.king_available_moves = []
        self.king_attacked_moves = []

    def look_if_king_in_checkmate_or_stalemate(self):
        self.king_attacked_moves = game.King_attacked_moves(self.board, self.color)
        self.king_available_moves = game.King_available_moves(self.board, self.color, self.king_attacked_moves)
        king_in_check_before_play = game.is_king_in_check(board=self.board,color=self.color,king_attacked_moves=self.king_attacked_moves,
        )
        all_legal_moves = self.get_all_legal_moves(self.board, self.color)

        if king_in_check_before_play:
            blocking_moves = self.get_checks_blocking_moves(self.board, self.color)
            #print("All legal moves:", blocking_moves)
            if blocking_moves == []:
                print("You are in checkmate")

                self.king_in_checkmate = True
                return True
        elif not king_in_check_before_play:
            if all_legal_moves == []:
                self.in_stalemate = True
                return True

    def play(self, move: str):
        # We are making a move and we check if the move is valid and if the king is in check after the move

        self.king_attacked_moves = game.King_attacked_moves(self.board, self.color)
        self.king_available_moves = game.King_available_moves(
            self.board, self.color, self.king_attacked_moves
        )
        king_in_check_before_play = game.is_king_in_check(
            board=self.board,
            color=self.color,
            king_attacked_moves=self.king_attacked_moves,
        )
        all_legal_moves = self.get_all_legal_moves(self.board, self.color)
        blocking_moves = self.get_checks_blocking_moves(self.board, self.color)
        #print("blocking moves:", blocking_moves)

        if king_in_check_before_play:
            if blocking_moves == []:
                print("You are in checkmate")
                self.king_in_checkmate = True
                return True
            print(
                "Your king is in check, you must play a move that gets your king out of check"
            )

            
            self.king_in_check = True
            simulation_king_in_check = self.test_play(move)
            if not simulation_king_in_check:
                return False
        elif not king_in_check_before_play:
            if all_legal_moves == []:
                self.in_stalemate = True
                return True
        simulation_ok = self.test_play(move)
        if not simulation_ok:
            return False

        # print("Simulation ok:", simulation_ok)
        self.king_attacked_moves = game.King_attacked_moves(
            self.simulation_board, self.color
        )
        self.king_available_moves = game.King_available_moves(
            self.simulation_board, self.color, self.king_attacked_moves
        )

        king_in_check = game.is_king_in_check(
            board=self.simulation_board,
            color=self.color,
            king_attacked_moves=self.king_attacked_moves,
        )

        if not king_in_check:
            # Apply the move to the actual board since it's valid and doesn't put the king in check.
            # print("King is not in check")
            self.king_in_check = False
            # deepcopy is not working so we have to copy the board manually
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.board[i][j] = self.simulation_board[i][j]

            # print(self.board)
            return True

        elif king_in_check:
            print("King is in check, move not allowed")
            return False

    def test_play(self, move: str):
        self.simulation_board = copy.deepcopy(self.board)
        pattern = r"[a-hA-H][1-8]-[a-hA-H][1-8]"
        move = move.strip()

        if not re.fullmatch(pattern, move):
            print("Invalid format, please use the format 'a2-a3' or 'A2-A3'")
            return False

        # print("Valid move format")

        # Convert move string to coordinates
        start_col = board_square[move[0]]
        start_row = board_square[move[1]]
        end_col = board_square[move[3]]
        end_row = board_square[move[4]]

        start_pawn = self.simulation_board[start_row][start_col]
        end_pawn = self.simulation_board[end_row][end_col]

        if start_pawn is None:
            # print("No piece at starting position")
            return False

        # Check if the piece belongs to the player
        if isinstance(start_pawn, Pawn) and start_pawn.get_color() != self.color:
            print("This is not your piece, you can only play your pieces")
            return False

        mov = (end_col - start_col, end_row - start_row)
        # Track whether this move is an en passant capture.
        is_en_passant = False
        en_passant_pawn = None

        if not game.is_movement_allowed(
            self.simulation_board, mov, start_pawn, position=(start_row, start_col)
        ):
            # print("Move not allowed for this piece")
            return False

        if start_pawn.get_type() == PawnType.PION:
            direction = -1 if self.color.name == "BLANC" else 1

            # Forward pawn moves must land on empty squares.
            if mov[0] == 0:
                if end_pawn is not None:
                    print("A pawn cannot move forward onto an occupied square")
                    return False

                # A two-square advance is only valid if the intermediate square is empty.
                if abs(mov[1]) == 2:
                    middle_row = start_row + direction
                    if self.simulation_board[middle_row][start_col] is not None:
                        print("A pawn cannot jump over another piece")
                        return False

            # Diagonal pawn moves are captures, including en passant on an empty destination square.
            elif abs(mov[0]) == 1 and mov[1] == direction:
                if end_pawn is None:
                    candidate = self.simulation_board[start_row][end_col]
                    # En passant is only allowed against the pawn that just advanced two squares.
                    if candidate is None or candidate != self.en_passant_target:
                        print("En passant not allowed")
                        return False
                    if (
                        candidate.get_type() != PawnType.PION
                        or candidate.get_color() == self.color
                    ):
                        print("En passant not allowed")
                        return False

                    is_en_passant = True
                    en_passant_pawn = candidate
                elif end_pawn.color == self.color:
                    print("You cannot take your own piece")
                    return False
            else:
                print("Move not allowed for this pawn")
                return False

        # Check for piece at the final destination
        if end_pawn is not None and end_pawn.color == self.color:
            # print("You cannot take your own piece")
            return False

        # Detect if the move is ROCK
        is_rock = False
        is_big_rock = False

        if (
            start_pawn.get_type() == PawnType.ROI
            and abs(end_col - start_col) == 2
            and not start_pawn.has_moved
        ):
            is_rock = True
            if end_col - start_col == -2:
                is_big_rock = True
                print("Long castle detected")
            else:
                print("Short castle detected")

        # Check if rock is valid
        if is_rock:
            tower_col = 0 if is_big_rock else 7
            tower = self.simulation_board[start_row][tower_col]

            # Check if tower has moved
            if (
                tower is None
                or tower.get_type() != PawnType.TOUR
                or tower.get_color() != self.color
                or tower.get_has_moved()
            ):
                print("Castle not allowed because the tower is not valid")
                return False

            # Check if piece on the way for ROCK (Tower and King)
            direction = -1 if is_big_rock else 1

            for col in range(start_col + direction, tower_col, direction):
                if self.simulation_board[start_row][col] is not None:
                    print(
                        "Castle not allowed because there is a piece between the king and the tower"
                    )
                    return False
            king_path_to_rock = game.King_castle_moves(
                self.simulation_board, self.color, direction
            )
            for move in king_path_to_rock:
                if move in self.king_attacked_moves:
                    print(
                        "Castle not allowed because the king would be in check on the way"
                    )
                    return False

        # print("Valid chess move")

        # Take opponent piece if there is one
        if is_en_passant:
            print("En passant")
            # Remove the adjacent pawn captured via en passant.
            self.take(en_passant_pawn)
        elif not is_rock and end_pawn is not None and end_pawn.color != self.color:
            # print("You take an opponent piece")
            self.take(end_pawn)

        # Move the tower for ROCK
        if is_rock:
            tower_col = 0 if is_big_rock else 7
            new_tower_col = start_col + (-1 if is_big_rock else 1)

            self.simulation_board[start_row][new_tower_col] = self.simulation_board[
                start_row
            ][tower_col]
            self.simulation_board[start_row][tower_col] = None
            self.simulation_board[start_row][new_tower_col].set_has_moved(True)

        # Move the piece
        start_pawn.set_has_moved(True)

        self.simulation_board[end_row][end_col] = start_pawn
        self.simulation_board[start_row][start_col] = None

        # Only a pawn that has just moved two squares can be captured en passant next turn.
        if start_pawn.get_type() == PawnType.PION and abs(end_row - start_row) == 2:
            self.en_passant_target = start_pawn
        else:
            self.en_passant_target = None

        return True

    def take(self, taken_piece: Pawn):
        # Add points for taken piece
        self.points += taken_piece.get_points()

        # Add taken piece to the list of taken pieces
        self.taken_pieces.append(taken_piece)

        # Remove taken piece from board
        for row in self.simulation_board:
            for i in range(len(row)):
                if row[i] == taken_piece:
                    row[i] = None

    def set_pinned_pieces_to_true(self, board, color):
        for row in board:
            for piece in row:
                if piece is not None and piece.get_color() == color:
                    piece.set_is_pinned(True)

    def get_all_legal_moves(self, board, color):
        legal_moves = []
        annotated_moves = game.get_all_annotated_moves(board, color)
        # print("Annotated moves:", annotated_moves)
        for move in annotated_moves:
            if self.test_play(move):
                
                self.king_attacked_moves = game.King_attacked_moves(self.simulation_board, self.color)
                if game.is_king_in_check(board = self.simulation_board, color = self.color, king_attacked_moves=self.king_attacked_moves):
                    pass
                else:
                    legal_moves.append(move)
        return legal_moves

    def get_checks_blocking_moves(self, board, color):
        blocking_moves = []
        annotated_moves = game.get_all_annotated_moves(board, color)
        for move in annotated_moves:
            if self.test_play(move):
                self.king_attacked_moves = game.King_attacked_moves(self.simulation_board, self.color)
                if not game.is_king_in_check(board = self.simulation_board, color = self.color, king_attacked_moves=self.king_attacked_moves):
                    blocking_moves.append(move)
        return blocking_moves

    def get_has_rock(self):
        return self.has_rock

    def get_en_passant_target(self):
        return self.en_passant_target

    def get_color(self):
        return self.color
