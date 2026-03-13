import tkinter as tk
from tkinter import messagebox

from color import Color
from history_helper import check_repetition, reset_history, save_board
from pawn import Pawn
from pawn_type import PawnType
from player import Player

LIGHT_SQUARE = "#F0D9B5"
DARK_SQUARE = "#B58863"
SELECTED_SQUARE = "#F6F669"
MOVE_SQUARE = "#A9CF54"
CHECK_SQUARE = "#E57373"


def init_board():
    return [
        [
            Pawn(PawnType.TOUR, Color.NOIR),
            Pawn(PawnType.CAVALIER, Color.NOIR),
            Pawn(PawnType.FOU, Color.NOIR),
            Pawn(PawnType.DAME, Color.NOIR),
            Pawn(PawnType.ROI, Color.NOIR),
            Pawn(PawnType.FOU, Color.NOIR),
            Pawn(PawnType.CAVALIER, Color.NOIR),
            Pawn(PawnType.TOUR, Color.NOIR),
        ],
        [Pawn(PawnType.PION, Color.NOIR) for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [Pawn(PawnType.PION, Color.BLANC) for _ in range(8)],
        [
            Pawn(PawnType.TOUR, Color.BLANC),
            Pawn(PawnType.CAVALIER, Color.BLANC),
            Pawn(PawnType.FOU, Color.BLANC),
            Pawn(PawnType.DAME, Color.BLANC),
            Pawn(PawnType.ROI, Color.BLANC),
            Pawn(PawnType.FOU, Color.BLANC),
            Pawn(PawnType.CAVALIER, Color.BLANC),
            Pawn(PawnType.TOUR, Color.BLANC),
        ],
    ]


class ChessGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Jeu d'échecs")
        self.root.resizable(False, False)

        self.board = init_board()
        self.player_white = Player(self.board, Color.BLANC)
        self.player_black = Player(self.board, Color.NOIR)
        self.current_player = self.player_white
        self.selected_square = None
        self.possible_moves = set()
        self.game_over = False
        reset_history()

        self.piece_symbols = {
            (Color.BLANC, PawnType.ROI): "♔",
            (Color.BLANC, PawnType.DAME): "♕",
            (Color.BLANC, PawnType.TOUR): "♖",
            (Color.BLANC, PawnType.FOU): "♗",
            (Color.BLANC, PawnType.CAVALIER): "♘",
            (Color.BLANC, PawnType.PION): "♙",
            (Color.NOIR, PawnType.ROI): "♚",
            (Color.NOIR, PawnType.DAME): "♛",
            (Color.NOIR, PawnType.TOUR): "♜",
            (Color.NOIR, PawnType.FOU): "♝",
            (Color.NOIR, PawnType.CAVALIER): "♞",
            (Color.NOIR, PawnType.PION): "♟",
        }

        self.build_layout()
        self.refresh_status("Cliquez sur une pièce pour commencer.")
        self.update_check_state()
        self.draw_board()

    def build_layout(self):
        container = tk.Frame(self.root, padx=12, pady=12)
        container.pack()

        left_panel = tk.Frame(container)
        left_panel.grid(row=0, column=0, sticky="n")

        right_panel = tk.Frame(container, padx=16)
        right_panel.grid(row=0, column=1, sticky="n")

        title = tk.Label(
            left_panel,
            text="Jeu d'échecs",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(pady=(0, 10))

        board_frame = tk.Frame(left_panel, bd=2, relief="groove")
        board_frame.pack()

        self.square_buttons = []
        for row in range(8):
            row_buttons = []
            for col in range(8):
                button = tk.Button(
                    board_frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Segoe UI Symbol", 22),
                    command=lambda r=row, c=col: self.on_square_click(r, c),
                    relief="flat",
                    bd=0,
                )
                button.grid(row=row, column=col, sticky="nsew")
                row_buttons.append(button)
            self.square_buttons.append(row_buttons)

        controls = tk.Frame(left_panel, pady=10)
        controls.pack(fill="x")

        self.reset_button = tk.Button(
            controls,
            text="Nouvelle partie",
            command=self.reset_game,
            font=("Segoe UI", 10, "bold"),
        )
        self.reset_button.pack(fill="x")

        self.turn_label = tk.Label(
            right_panel,
            text="",
            anchor="w",
            justify="left",
            font=("Segoe UI", 12, "bold"),
        )
        self.turn_label.pack(fill="x", pady=(0, 8))

        self.status_label = tk.Label(
            right_panel,
            text="",
            anchor="w",
            justify="left",
            wraplength=280,
            font=("Segoe UI", 10),
            fg="#333333",
        )
        self.status_label.pack(fill="x", pady=(0, 12))

        self.white_info = tk.Label(
            right_panel,
            text="",
            anchor="w",
            justify="left",
            font=("Segoe UI", 10),
            wraplength=280,
        )
        self.white_info.pack(fill="x", pady=(0, 8))

        self.black_info = tk.Label(
            right_panel,
            text="",
            anchor="w",
            justify="left",
            font=("Segoe UI", 10),
            wraplength=280,
        )
        self.black_info.pack(fill="x", pady=(0, 12))

        help_text = (
            "Utilisation :\n"
            "- Cliquez sur une pièce de la couleur au trait.\n"
            "- Cliquez ensuite sur la case de destination.\n"
            "- Le roque fonctionne en déplaçant le roi de deux cases.\n"
            "- La validation des coups utilise le moteur existant."
        )
        self.help_label = tk.Label(
            right_panel,
            text=help_text,
            anchor="w",
            justify="left",
            font=("Segoe UI", 9),
            wraplength=280,
            fg="#555555",
        )
        self.help_label.pack(fill="x")

    def reset_game(self):
        self.board = init_board()
        self.player_white = Player(self.board, Color.BLANC)
        self.player_black = Player(self.board, Color.NOIR)
        self.current_player = self.player_white
        self.selected_square = None
        self.possible_moves = set()
        self.game_over = False
        reset_history()
        self.refresh_status("Nouvelle partie démarrée.")
        self.update_check_state()
        self.draw_board()

    def get_opponent(self, player: Player) -> Player:
        return self.player_black if player.color == Color.BLANC else self.player_white

    def piece_to_symbol(self, piece):
        if piece is None:
            return ""
        return self.piece_symbols.get((piece.get_color(), piece.get_type()), "?")

    def coords_to_notation(self, row: int, col: int) -> str:
        files = "abcdefgh"
        rank = 8 - row
        return f"{files[col]}{rank}"

    def notation_to_coords(self, square: str):
        files = "abcdefgh"
        col = files.index(square[0].lower())
        row = 8 - int(square[1])
        return row, col

    def build_move_notation(
        self, start_row: int, start_col: int, end_row: int, end_col: int
    ) -> str:
        return f"{self.coords_to_notation(start_row, start_col)}-{self.coords_to_notation(end_row, end_col)}"

    def get_legal_moves_for_square(self, row: int, col: int):
        piece = self.board[row][col]
        if piece is None or piece.get_color() != self.current_player.color:
            return set()

        legal_moves = set()
        annotated_moves = self.current_player.get_all_legal_moves(
            self.board, self.current_player.color
        )

        for move in annotated_moves:
            start, end = move.split("-")
            start_row, start_col = self.notation_to_coords(start)
            end_row, end_col = self.notation_to_coords(end)

            if start_row == row and start_col == col:
                legal_moves.add((end_row, end_col))

        return legal_moves

    def get_square_color(self, row: int, col: int) -> str:
        return LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE

    def get_king_square_in_check(self):
        attacked = self.current_player.king_attacked_moves
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if (
                    piece is not None
                    and piece.get_type() == PawnType.ROI
                    and piece.get_color() == self.current_player.color
                    and (row, col) in attacked
                ):
                    return row, col
        return None

    def draw_board(self):
        self.turn_label.config(text=f"Tour : {self.current_player.color.value}")

        white_taken = (
            " ".join(self.piece_to_symbol(p) for p in self.player_white.taken_pieces)
            or "Aucune"
        )
        black_taken = (
            " ".join(self.piece_to_symbol(p) for p in self.player_black.taken_pieces)
            or "Aucune"
        )

        self.white_info.config(
            text=(
                f"Blanc\n"
                f"Points : {self.player_white.points}\n"
                f"Pièces prises : {white_taken}"
            )
        )
        self.black_info.config(
            text=(
                f"Noir\n"
                f"Points : {self.player_black.points}\n"
                f"Pièces prises : {black_taken}"
            )
        )

        king_in_check_square = self.get_king_square_in_check()

        for row in range(8):
            for col in range(8):
                base_color = self.get_square_color(row, col)

                if self.selected_square == (row, col):
                    bg = SELECTED_SQUARE
                elif (row, col) in self.possible_moves:
                    bg = MOVE_SQUARE
                elif king_in_check_square == (row, col):
                    bg = CHECK_SQUARE
                else:
                    bg = base_color

                self.square_buttons[row][col].config(
                    text=self.piece_to_symbol(self.board[row][col]),
                    bg=bg,
                    activebackground=bg,
                    fg="#111111",
                    disabledforeground="#111111",
                )

    def refresh_status(self, message: str):
        self.status_label.config(text=message)

    def update_check_state(self):
        self.current_player.look_if_king_in_checkmate()

    def on_square_click(self, row: int, col: int):
        if self.game_over:
            return

        piece = self.board[row][col]

        if self.selected_square is None:
            if piece is None:
                self.refresh_status("Sélectionnez une pièce.")
                return

            if piece.get_color() != self.current_player.color:
                self.refresh_status("Vous devez sélectionner une de vos pièces.")
                return

            self.selected_square = (row, col)
            self.possible_moves = self.get_legal_moves_for_square(row, col)

            if not self.possible_moves:
                self.refresh_status("Cette pièce n'a pas de coup légal disponible.")
            else:
                square_name = self.coords_to_notation(row, col)
                self.refresh_status(
                    f"Pièce sélectionnée : {square_name}. Choisissez une destination."
                )

            self.draw_board()
            return

        start_row, start_col = self.selected_square

        if (row, col) == self.selected_square:
            self.selected_square = None
            self.possible_moves = set()
            self.refresh_status("Sélection annulée.")
            self.draw_board()
            return

        if piece is not None and piece.get_color() == self.current_player.color:
            self.selected_square = (row, col)
            self.possible_moves = self.get_legal_moves_for_square(row, col)

            if not self.possible_moves:
                self.refresh_status("Cette pièce n'a pas de coup légal disponible.")
            else:
                square_name = self.coords_to_notation(row, col)
                self.refresh_status(
                    f"Pièce sélectionnée : {square_name}. Choisissez une destination."
                )

            self.draw_board()
            return

        move = self.build_move_notation(start_row, start_col, row, col)
        self.try_play_move(move)

    def try_play_move(self, move: str):
        player = self.current_player
        opponent = self.get_opponent(player)

        success = player.play(move, opponent=opponent, silent=True)
        self.selected_square = None
        self.possible_moves = set()

        if not success:
            message = player.last_message or "Coup invalide."
            self.refresh_status(message)
            self.update_check_state()
            self.draw_board()
            return

        save_board(
            self.board, self.player_white, self.player_black, self.current_player
        )
        if check_repetition():
            self.game_over = True
            self.refresh_status(
                "Nul par répétition : la même position s'est répétée 3 fois."
            )
            self.draw_board()
            messagebox.showinfo("Partie terminée", "Nul par répétition.")
            return

        self.current_player = opponent
        self.update_check_state()

        if self.current_player.king_in_checkmate:
            winner = self.get_opponent(self.current_player)
            self.game_over = True
            self.refresh_status(f"Échec et mat ! {winner.color.value} gagne.")
            self.draw_board()
            messagebox.showinfo(
                "Partie terminée",
                f"Échec et mat ! {winner.color.value} gagne.",
            )
            return

        if self.current_player.king_in_check:
            self.refresh_status(f"{self.current_player.color.value} est en échec.")
        else:
            self.refresh_status(f"Coup joué : {move}")

        self.draw_board()


def main():
    root = tk.Tk()
    ChessGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
