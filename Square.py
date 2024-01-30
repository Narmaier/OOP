BLACK = "B"
WHITE = "W"


class Square:
    def __init__(self, piece):
        self.piece = piece
        self.counterattack = []
        self.attack = {}
        self.pawn_moves = {}
        self.value = 0
        if piece is not None:
            self.value = piece.value

    def change_piece(self, new_piece):
        self.piece = new_piece
        self.value = new_piece.value

    def delete_piece(self):
        self.piece.clear_statements()
        self.piece = None
        self.value = 0

    def set_statement(self, attack, counterattack):
        self.counterattack.append(counterattack)
        self.attack[attack[0]] = attack[1]

    def clear_statement(self):
        self.attack = {}
        self.counterattack = []

    def check_space(self):
        return self.piece is None

    def __str__(self):
        if self.piece is None:
            return "*"
        else:
            if self.piece.color == BLACK:
                return str(self.piece).lower()
            else:
                return str(self.piece)

