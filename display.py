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


def display_board(board) -> str:
	files = "ABCDEFGH"

	def header_or_footer() -> str:
		return "    " + " ".join(f" {f} " for f in files)

	# lignes de séparation type +---+---+...
	sep = "    +" + "+".join(["---"] * 8) + "+"

	lines: list[str] = [header_or_footer()]
	for row in range(8):
		rank = 8 - row
		lines.append(sep)
		cells = []
		for col in range(8):
			piece = board[row][col]
			cells.append(piece_to_emoji(piece))
		lines.append(f" {rank}  | " + " | ".join(cells) + " |")
	lines.append(sep)
	lines.append(header_or_footer())
	return "\n".join(lines)
