from color import Color
from pawn import Pawn
from pawn_type import PawnType

def piece_to_emoji(pawn: Pawn):
    if pawn is None:
        return " "

    type = pawn.get_type()
    color = pawn.get_color()

    BLACK = {
		PawnType.ROI: "♔",
		PawnType.DAME: "♕",
		PawnType.TOUR: "♖",
		PawnType.FOU: "♗",
		PawnType.CAVALIER: "♘",
		PawnType.PION: "♙",
	}

    WHITE = {
		PawnType.ROI: "♚",
		PawnType.DAME: "♛",
		PawnType.TOUR: "♜",
		PawnType.FOU: "♝",
		PawnType.CAVALIER: "♞",
		PawnType.PION: "♟",
	}

    if color == Color.BLANC:
        return WHITE.get(type, "?")
    else:
        return BLACK.get(type, "?")


def display_board(board, attacks = []) -> str:
	files = "ABCDEFGH"

	def header_or_footer() -> str:
		return "    " + " ".join(f" {f} " for f in files)

	sep = "    +" + "+".join(["---"] * 8) + "+"

	lines: list[str] = [header_or_footer()]
	for row in range(8):
		rank = 8 - row
		lines.append(sep)
		cells = []
		for col in range(8):
			piece = board[row][col]
			cell = piece_to_emoji(piece)
			if (row, col) in attacks:
				cell = f"\033[41m{cell}\033[0m"
			cells.append(cell)
		lines.append(f" {rank}  | " + " | ".join(cells) + " |")
	lines.append(sep)
	lines.append(header_or_footer())
	print("\n".join(lines))


def display_points(player_white, player_black) -> None:
	white_taken = " ".join(piece_to_emoji(piece) for piece in player_white.taken_pieces) or "Aucune"
	black_taken = " ".join(piece_to_emoji(piece) for piece in player_black.taken_pieces) or "Aucune"

	print("\nPièces prises :")
	print(f"Blanc : {white_taken} | Points : {player_white.points}")
	print(f"Noir  : {black_taken} | Points : {player_black.points}")

	advantage = player_white.points - player_black.points
	if advantage > 0:
		print(f"Avantage : Blanc +{advantage}")
	elif advantage < 0:
		print(f"Avantage : Noir +{abs(advantage)}")
	else:
		print("Avantage : Égalité")