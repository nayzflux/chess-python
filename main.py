from frontend import title
from color import Color
from game import play_round
from history_helper import check_repetition, save_board
from pawn import Pawn
from pawn_type import PawnType
from player import Player

title()

test_rock_board = [
    [Pawn(PawnType.TOUR, Color.NOIR), Pawn(PawnType.CAVALIER, Color.NOIR), None, None, Pawn(PawnType.ROI, Color.NOIR), Pawn(PawnType.FOU, Color.NOIR), None, Pawn(PawnType.TOUR, Color.NOIR)],
    [Pawn(PawnType.PION, Color.NOIR) for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [Pawn(PawnType.PION, Color.BLANC) for _ in range(8)],
    [Pawn(PawnType.TOUR, Color.BLANC), None, None, None, Pawn(PawnType.ROI, Color.BLANC), None, None, Pawn(PawnType.TOUR, Color.BLANC)],
]

test_stalemate = [
    [Pawn(PawnType.ROI, Color.NOIR), None, None, None, None, None, None, None],
    [None, None, None, Pawn(PawnType.DAME, Color.BLANC), None, None, None, None],
    [Pawn(PawnType.ROI, Color.BLANC), *[None for _ in range(7)]],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None for _ in range(8)],
]


sequence_board = [
    [None, None, None, None, Pawn(PawnType.ROI, Color.NOIR), None, None, None],
    [None, None, None, Pawn(PawnType.PION, Color.NOIR), Pawn(PawnType.PION, Color.NOIR), Pawn(PawnType.PION, Color.NOIR), None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, Pawn(PawnType.TOUR, Color.NOIR), None],
    [None, None, None, None, Pawn(PawnType.ROI, Color.BLANC), None, None, Pawn(PawnType.DAME, Color.BLANC)],
]

sequence_board_2 = [
    [None, None, None, None, None, None, None, None],
    [None, None, None, Pawn(PawnType.PION, Color.NOIR), Pawn(PawnType.PION, Color.NOIR), Pawn(PawnType.PION, Color.NOIR), None, None],
    [None, None, None, Pawn(PawnType.ROI, Color.NOIR), None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, Pawn(PawnType.PION, Color.BLANC), Pawn(PawnType.PION, Color.BLANC), None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, Pawn(PawnType.TOUR, Color.NOIR), None],
    [None, None, None, None, Pawn(PawnType.ROI, Color.BLANC), None, None, Pawn(PawnType.DAME, Color.BLANC)],
]

test_castling_board = [
    [Pawn(PawnType.TOUR, Color.NOIR), None, None, None, Pawn(PawnType.ROI, Color.NOIR), None, None, Pawn(PawnType.TOUR, Color.NOIR)],
    [None for _ in range(8)],
    [None, None, Pawn(PawnType.FOU, Color.NOIR), None, None, Pawn(PawnType.CAVALIER, Color.NOIR), None, None],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None, None, Pawn(PawnType.FOU, Color.BLANC), None, None, Pawn(PawnType.CAVALIER, Color.BLANC), None, None],
    [None for _ in range(8)],
    [Pawn(PawnType.TOUR, Color.BLANC), None, None, None, Pawn(PawnType.ROI, Color.BLANC), None, None, Pawn(PawnType.TOUR, Color.BLANC)],
]

test_check_board = [
    [Pawn(PawnType.TOUR, Color.NOIR), None, None, None, Pawn(PawnType.ROI, Color.NOIR), None, None, Pawn(PawnType.TOUR, Color.NOIR)],
    [None, Pawn(PawnType.PION, Color.NOIR), None, None, None, None, Pawn(PawnType.PION, Color.NOIR), None],
    [None, None, Pawn(PawnType.CAVALIER, Color.NOIR), None, None, Pawn(PawnType.FOU, Color.NOIR), None, None],
    [None for _ in range(8)],
    [None for _ in range(8)],
    [None, None, Pawn(PawnType.FOU, Color.BLANC), None, None, Pawn(PawnType.CAVALIER, Color.BLANC), None, None],
    [None, Pawn(PawnType.PION, Color.BLANC), None, None, None, None, Pawn(PawnType.PION, Color.BLANC), None],
    [Pawn(PawnType.TOUR, Color.BLANC), None, None, None, Pawn(PawnType.ROI, Color.BLANC), None, None, Pawn(PawnType.TOUR, Color.BLANC)],
]

def init_board():
    board = [
        [Pawn(PawnType.TOUR, Color.NOIR), Pawn(PawnType.CAVALIER, Color.NOIR), Pawn(PawnType.FOU, Color.NOIR), Pawn(PawnType.DAME, Color.NOIR), Pawn(PawnType.ROI, Color.NOIR), Pawn(PawnType.FOU, Color.NOIR), Pawn(PawnType.CAVALIER, Color.NOIR), Pawn(PawnType.TOUR, Color.NOIR)],
        [Pawn(PawnType.PION, Color.NOIR) for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [Pawn(PawnType.PION, Color.BLANC) for _ in range(8)],
        [Pawn(PawnType.TOUR, Color.BLANC), Pawn(PawnType.CAVALIER, Color.BLANC), Pawn(PawnType.FOU, Color.BLANC), Pawn(PawnType.DAME, Color.BLANC), Pawn(PawnType.ROI, Color.BLANC), Pawn(PawnType.FOU, Color.BLANC), Pawn(PawnType.CAVALIER, Color.BLANC), Pawn(PawnType.TOUR, Color.BLANC)],
    ]
    return board


if __name__ == "__main__":
    # board = init_board()
    board = sequence_board_2

    player_white = Player(board, Color.BLANC)
    player_black = Player(board, Color.NOIR)

    current_player = player_white
    round_count = 1
    run = True
    while run:
        opponent = player_black if current_player.color == Color.BLANC else player_white

        # Save board state for repetition draw
        save_board(board, player_white, player_black, current_player)

        # Check for repetion draw
        if check_repetition():
            print("==================================")
            print("NUL par répétition !")
            print("L'exact même position c'est répétée 3 fois sur l'échéquier.")
            print("==================================")
            break

        play_round(board, current_player, opponent, round_count)

        if current_player.king_in_checkmate:
            print(f"Checkmate! {opponent.color.value} wins!")
            run = False
            break
        if current_player.in_stalemate:
            print(f"It's a draw ! {current_player.color.value} has no move!")
            run = False
        round_count += 1
        current_player = (
            player_black if current_player.color == Color.BLANC else player_white
        )