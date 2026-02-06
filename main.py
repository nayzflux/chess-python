

from color import Color
from game import play_round
from pawn import Pawn
from pawn_type import PawnType
from display import display_board
from player import Player

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
    board = init_board()

    player_white = Player(board, Color.BLANC)
    player_black = Player(board, Color.NOIR)

    current_player = player_white
    round_count = 1
    
    while True:
        # TODO: Check win condition
        play_round(board, current_player, round_count)
        round_count += 1
        current_player = player_black if current_player.color == Color.BLANC else player_white