class Pawn:
    def __init__(self, pawn_type, color):
        self.pawn_type = pawn_type
        self.color = color
        self.has_moved = False

    def get_type(self):
        return self.pawn_type
    
    def get_color(self):
        return self.color
    
    def get_has_moved(self):
        return self.has_moved

    def set_has_moved(self, has_moved: bool):
        self.has_moved = has_moved