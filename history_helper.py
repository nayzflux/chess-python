import hashlib

from typing_extensions import Dict

from pawn import Pawn
from player import Player

# Historique des hash des états de jeu
history: Dict[str, int] = {}


# Créer un hash depuis un string
def hash(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# Verifier si la position est 3 fois la même
def check_repetition():
    # print(history)
    for occurence in history.values():
        if occurence >= 3:
            return True

    return False


# Sauvegarder l'état de jeu dans un hash
def save_board(board, player1: Player, player2: Player, current_player: Player):
    board_hash = compute_board_hash(board)
    player1_hash = compute_player_hash(player1)
    player2_hash = compute_player_hash(player2)
    current_player_color = current_player.get_color()

    game_hash = hash(
        f"{board_hash}:{player1_hash}:{player2_hash}:{current_player_color}"
    )

    if game_hash in history:
        history[game_hash] += 1
    else:
        history[game_hash] = 1


# Calculer le hash de l'état d'un joueur
def compute_player_hash(player: Player):
    en_passant_pawn = player.get_en_passant_target()
    en_passant_hash = compute_pawn_hash(en_passant_pawn)
    has_rock = player.get_has_rock()

    data = f"{en_passant_hash}:{has_rock}"

    return hash(data)


# Calculer le hash des positions
def compute_board_hash(board):
    data = ""

    for i in range(8):
        for j in range(8):
            pawn_hash = compute_pawn_hash(board[i][j])
            data += f"{pawn_hash}:"

    return hash(data)


# Calculer le hash de l'état du pion
def compute_pawn_hash(pawn: Pawn | None):
    if pawn is None:
        return "0"

    color = pawn.get_color()
    type = pawn.get_type()
    has_moved = pawn.get_has_moved()
    is_pinned = pawn.get_is_pinned()

    data = f"{color}:{type}:{has_moved}:{is_pinned}"

    return hash(data)
