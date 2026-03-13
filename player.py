import copy
import re

import game
from color import Color
from pawn import Pawn
from pawn_type import PawnType

board_square = {
    # Files
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    # Ranks
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
    "8": 0,
}


class Player:
    def __init__(self, board, color: Color):
        self.en_passant_target: Pawn | None = None
        self.has_rock = False
        self.has_win = False
        self.color = color
        self.king_in_check = False
        self.king_in_checkmate = False
        self.board = board
        self.taken_pieces = []
        self.points = 0
        self.simulation_board = []
        self.king_available_moves = []
        self.king_attacked_moves = []
        self.last_message = ""

    def _set_message(self, message: str, silent: bool = False):
        self.last_message = message
        if message and not silent:
            print(message)

    def clear_message(self):
        self.last_message = ""

    def sync_en_passant_from(self, other_player: "Player"):
        self.en_passant_target = other_player.en_passant_target

    def _copy_board_into_self_board(self, source_board):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j] = source_board[i][j]

    def _build_snapshot(self):
        return {
            "board": copy.deepcopy(self.board),
            "en_passant_target": self.en_passant_target,
            "has_rock": self.has_rock,
            "points": self.points,
            "taken_pieces": list(self.taken_pieces),
            "king_in_check": self.king_in_check,
            "king_in_checkmate": self.king_in_checkmate,
            "king_available_moves": list(self.king_available_moves),
            "king_attacked_moves": list(self.king_attacked_moves),
            "last_message": self.last_message,
            "simulation_board": copy.deepcopy(self.simulation_board)
            if self.simulation_board
            else [],
        }

    def _restore_snapshot(self, snapshot):
        self._copy_board_into_self_board(snapshot["board"])
        self.en_passant_target = snapshot["en_passant_target"]
        self.has_rock = snapshot["has_rock"]
        self.points = snapshot["points"]
        self.taken_pieces = snapshot["taken_pieces"]
        self.king_in_check = snapshot["king_in_check"]
        self.king_in_checkmate = snapshot["king_in_checkmate"]
        self.king_available_moves = snapshot["king_available_moves"]
        self.king_attacked_moves = snapshot["king_attacked_moves"]
        self.last_message = snapshot["last_message"]
        self.simulation_board = snapshot["simulation_board"]

    def _apply_simulation_to_board(self, simulated_board):
        self._copy_board_into_self_board(simulated_board)
        self.simulation_board = copy.deepcopy(simulated_board)

    def _coords_to_move(self, start_row, start_col, end_row, end_col):
        files = "abcdefgh"
        start = f"{files[start_col]}{8 - start_row}"
        end = f"{files[end_col]}{8 - end_row}"
        return f"{start}-{end}"

    def look_if_king_in_checkmate(self):
        self.king_attacked_moves = game.King_attacked_moves(self.board, self.color)
        self.king_available_moves = game.King_available_moves(
            self.board, self.color, self.king_attacked_moves
        )
        king_in_check_before_play = game.is_king_in_check(
            board=self.board,
            color=self.color,
            king_attacked_moves=self.king_attacked_moves,
        )

        if king_in_check_before_play:
            blocking_moves = self.get_checks_blocking_moves(self.board, self.color)
            if blocking_moves == []:
                self._set_message("You are in checkmate")
                self.king_in_checkmate = True
                return True

        self.king_in_checkmate = False
        return False

    def play(self, move: str, opponent: "Player | None" = None, silent: bool = False):
        self.clear_message()

        if opponent is not None:
            self.sync_en_passant_from(opponent)

        self.king_attacked_moves = game.King_attacked_moves(self.board, self.color)
        self.king_available_moves = game.King_available_moves(
            self.board, self.color, self.king_attacked_moves
        )

        king_in_check_before_play = game.is_king_in_check(
            board=self.board,
            color=self.color,
            king_attacked_moves=self.king_attacked_moves,
        )
        blocking_moves = self.get_checks_blocking_moves(self.board, self.color)

        if king_in_check_before_play and move not in blocking_moves:
            self.king_in_check = True
            self._set_message(
                "Your king is in check, you must play a move that gets your king out of check",
                silent,
            )
            return False

        snapshot = self._build_snapshot()
        simulation_ok = self.test_play(move, silent=True, apply_score=False)

        if not simulation_ok:
            simulated_message = self.last_message or "Move not allowed"
            self._restore_snapshot(snapshot)
            self._set_message(simulated_message, silent)
            return False

        simulated_board = copy.deepcopy(self.simulation_board)
        simulated_en_passant_target = self.en_passant_target
        simulated_has_rock = self.has_rock
        simulated_attacked_moves = game.King_attacked_moves(simulated_board, self.color)
        simulated_available_moves = game.King_available_moves(
            simulated_board, self.color, simulated_attacked_moves
        )
        king_in_check_after_play = game.is_king_in_check(
            board=simulated_board,
            color=self.color,
            king_attacked_moves=simulated_attacked_moves,
        )

        self._restore_snapshot(snapshot)

        if king_in_check_after_play:
            self.king_in_check = True
            self._set_message("King is in check, move not allowed", silent)
            return False

        commit_ok = self.test_play(move, silent=silent, apply_score=True)
        if not commit_ok:
            return False

        self.king_in_check = False
        self.king_in_checkmate = False
        self.king_attacked_moves = simulated_attacked_moves
        self.king_available_moves = simulated_available_moves
        self.has_rock = simulated_has_rock
        self.en_passant_target = simulated_en_passant_target
        self._apply_simulation_to_board(simulated_board)

        if opponent is not None:
            opponent.en_passant_target = self.en_passant_target

        return True

    def test_play(self, move: str, silent: bool = True, apply_score: bool = False):
        self.simulation_board = copy.deepcopy(self.board)
        pattern = r"[a-hA-H][1-8]-[a-hA-H][1-8]"
        move = move.strip()

        if not re.fullmatch(pattern, move):
            self._set_message(
                "Invalid format, please use the format 'a2-a3' or 'A2-A3'", silent
            )
            return False

        start_col = board_square[move[0]]
        start_row = board_square[move[1]]
        end_col = board_square[move[3]]
        end_row = board_square[move[4]]

        start_pawn = self.simulation_board[start_row][start_col]
        end_pawn = self.simulation_board[end_row][end_col]

        if start_pawn is None:
            self._set_message("No piece at starting position", silent)
            return False

        if not isinstance(start_pawn, Pawn):
            self._set_message("Invalid piece at starting position", silent)
            return False

        if start_pawn.get_color() != self.color:
            self._set_message(
                "This is not your piece, you can only play your pieces", silent
            )
            return False

        mov = (end_col - start_col, end_row - start_row)
        is_en_passant = False
        en_passant_pawn = None
        captured_piece = None
        new_has_rock = self.has_rock

        if not game.is_movement_allowed(
            self.simulation_board, mov, start_pawn, position=(start_row, start_col)
        ):
            self._set_message("Move not allowed for this piece", silent)
            return False

        if start_pawn.get_type() == PawnType.PION:
            direction = -1 if self.color == Color.BLANC else 1

            if mov[0] == 0:
                if end_pawn is not None:
                    self._set_message(
                        "A pawn cannot move forward onto an occupied square", silent
                    )
                    return False

                if abs(mov[1]) == 2:
                    middle_row = start_row + direction
                    if self.simulation_board[middle_row][start_col] is not None:
                        self._set_message(
                            "A pawn cannot jump over another piece", silent
                        )
                        return False

            elif abs(mov[0]) == 1 and mov[1] == direction:
                if end_pawn is None:
                    candidate = self.simulation_board[start_row][end_col]
                    if candidate is None or candidate != self.en_passant_target:
                        self._set_message("En passant not allowed", silent)
                        return False

                    if (
                        not isinstance(candidate, Pawn)
                        or candidate.get_type() != PawnType.PION
                        or candidate.get_color() == self.color
                    ):
                        self._set_message("En passant not allowed", silent)
                        return False

                    is_en_passant = True
                    en_passant_pawn = candidate
                elif end_pawn.get_color() == self.color:
                    self._set_message("You cannot take your own piece", silent)
                    return False
            else:
                self._set_message("Move not allowed for this pawn", silent)
                return False

        if end_pawn is not None and end_pawn.get_color() == self.color:
            self._set_message("You cannot take your own piece", silent)
            return False

        is_rock = False
        is_big_rock = False

        if (
            start_pawn.get_type() == PawnType.ROI
            and abs(end_col - start_col) == 2
            and not start_pawn.get_has_moved()
        ):
            is_rock = True
            if end_col - start_col == -2:
                is_big_rock = True

        if is_rock:
            tower_col = 0 if is_big_rock else 7
            tower = self.simulation_board[start_row][tower_col]

            if (
                tower is None
                or not isinstance(tower, Pawn)
                or tower.get_type() != PawnType.TOUR
                or tower.get_color() != self.color
                or tower.get_has_moved()
            ):
                self._set_message(
                    "Castle not allowed because the rook is not valid", silent
                )
                return False

            direction = -1 if is_big_rock else 1

            for col in range(start_col + direction, tower_col, direction):
                if self.simulation_board[start_row][col] is not None:
                    self._set_message(
                        "Castle not allowed because there is a piece between the king and the rook",
                        silent,
                    )
                    return False

            king_path_to_rock = game.King_castle_moves(
                self.simulation_board, self.color, direction
            )
            for move_to_check in king_path_to_rock:
                if move_to_check in self.king_attacked_moves:
                    self._set_message(
                        "Castle not allowed because the king would be in check on the way",
                        silent,
                    )
                    return False

            new_has_rock = True

        if is_en_passant:
            captured_piece = en_passant_pawn
        elif (
            not is_rock and end_pawn is not None and end_pawn.get_color() != self.color
        ):
            captured_piece = end_pawn

        if is_rock:
            tower_col = 0 if is_big_rock else 7
            new_tower_col = start_col + (-1 if is_big_rock else 1)

            self.simulation_board[start_row][new_tower_col] = self.simulation_board[
                start_row
            ][tower_col]
            self.simulation_board[start_row][tower_col] = None
            self.simulation_board[start_row][new_tower_col].set_has_moved(True)

        if captured_piece is not None:
            self.take(captured_piece, apply_score=apply_score)

        moved_piece = self.simulation_board[start_row][start_col]
        moved_piece.set_has_moved(True)
        self.simulation_board[end_row][end_col] = moved_piece
        self.simulation_board[start_row][start_col] = None

        if moved_piece.get_type() == PawnType.PION and abs(end_row - start_row) == 2:
            self.en_passant_target = moved_piece
        else:
            self.en_passant_target = None

        self.has_rock = new_has_rock
        return True

    def take(self, taken_piece: Pawn, apply_score: bool = True):
        if apply_score:
            self.points += taken_piece.get_points()
            self.taken_pieces.append(taken_piece)

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
        snapshot = self._build_snapshot()

        for start_row in range(8):
            for start_col in range(8):
                piece = board[start_row][start_col]
                if piece is None or piece.get_color() != color:
                    continue

                for end_row in range(8):
                    for end_col in range(8):
                        if start_row == end_row and start_col == end_col:
                            continue

                        move = self._coords_to_move(
                            start_row, start_col, end_row, end_col
                        )
                        simulation_ok = self.test_play(
                            move, silent=True, apply_score=False
                        )

                        if not simulation_ok:
                            self._restore_snapshot(snapshot)
                            continue

                        simulated_board = copy.deepcopy(self.simulation_board)
                        simulated_attacked_moves = game.King_attacked_moves(
                            simulated_board, self.color
                        )

                        if not game.is_king_in_check(
                            board=simulated_board,
                            color=self.color,
                            king_attacked_moves=simulated_attacked_moves,
                        ):
                            legal_moves.append(move)

                        self._restore_snapshot(snapshot)

        return legal_moves

    def get_checks_blocking_moves(self, board, color):
        return self.get_all_legal_moves(board, color)

    def get_has_rock(self):
        return self.has_rock

    def get_en_passant_target(self):
        return self.en_passant_target

    def get_color(self):
        return self.color
