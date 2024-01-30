from Square import Square, BLACK

ATTACK = 0
REPLACE = 1


# не создавать коор. заведомо за границей#TODO


class Piece:
    def __init__(self, position, color):
        self.color = color
        self.line, self.column = position[0], position[1]
        self.attack = {}
        self.counterattack = []
        self.value = 0

    def check_move(self, new_position):
        if self.attack.get(new_position) is not None:
            if self.attack.get(new_position) == ():
                return False
            else:
                return True
        else:
            return None

    def set_available_move(self, board: [Square], directions=None):
        if directions is None:
            directions = []
        for direction in directions:
            line, column = self.line, self.column
            while 0 <= line + direction[0] < 8 and 0 <= column + direction[1] < 8:
                line += direction[0]
                column += direction[1]
                if board[line][column].piece is None:
                    self.attack[(line, column)] = ()
                else:
                    if board[line][column].piece.color != self.color:
                        self.attack[(line, column)] = (line, column)
                        break
                    else:
                        self.counterattack.append((line, column))
                        break

    def move(self, new_position, board: [Square]):
        self.line, self.column = new_position[0], new_position[1]
        self.clear_statements()
        self.set_available_move(board)

    def clear_statements(self):
        self.attack = {}
        self.counterattack = []

    def pos(self):
        return self.line, self.column


class Pawn(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.value = 1

        if color == BLACK:
            self.texture = "svg/pieces/black_pawn.svg"
            self.direction = 1
        else:
            self.direction = -1
            self.texture = "svg/pieces/white_pawn.svg"

        self.has_moved = False
        self.double_move = False

    def set_available_move(self, board: [Square], directions=None):
        self.attack = {}
        self.counterattack = []
        line, column = self.line, self.column
        if 0 <= line + self.direction < 8 and 0 <= column < 8 and board[line + self.direction][column].piece is None:
            self.attack[(line + self.direction, column)] = ()
            if not self.has_moved and board[line + 2 * self.direction][column].piece is None:
                self.attack[(line + 2 * self.direction, column)] = ()

        if 0 <= line + self.direction < 8:
            if 0 <= column + 1 < 8 and board[line + self.direction][column + 1].piece is not None:
                if board[line + self.direction][column + 1].piece.color != self.color:
                    self.attack[(line + self.direction, column + 1)] = (line + self.direction, column + 1)
                else:
                    self.counterattack.append((line + self.direction, column + 1))

            if 0 <= column - 1 < 8 and board[line + self.direction][column - 1].piece is not None:
                if board[line + self.direction][column - 1].piece.color != self.color:
                    self.attack[(line + self.direction, column - 1)] = (line + self.direction, column - 1)
                else:
                    self.counterattack.append((line + self.direction, column - 1))

    def move(self, new_position, board: [Square]):
        super().move(new_position, board)
        self.has_moved = True
        if not self.double_move and new_position[0] == self.line + self.direction * 2:
            self.double_move = True

    def promote(self, promote_class, position, color):
        self.__class__ = promote_class
        self.__init__(position, color)

    def __str__(self):
        return "P"



class Knight(Piece):

    def __init__(self, position, color):
        super().__init__(position, color)
        self.value = 30
        if color == BLACK:
            self.texture = "svg/pieces/black_knight.svg"
        else:
            self.texture = "svg/pieces/white_knight.svg"

    def set_available_move(self, board: [Square], direction=None):
        for square in [(line + self.line, column + self.column) for line in [-2, -1, 1, 2] for column in [-2, -1, 1, 2]
                       if abs(line) != abs(column) if 0 <= line + self.line < 8 if 0 <= column + self.column < 8]:
            if board[square[0]][square[1]].piece is not None:
                if board[square[0]][square[1]].piece.color == self.color:
                    self.counterattack.append(square)
                else:
                    self.attack[square] = square
            else:
                self.attack[square] = ()

    def __str__(self):
        return "N"


class Rook(Piece):

    def __init__(self, position, color):
        super().__init__(position, color)
        self.moved = False
        self.value = 50
        if color == BLACK:
            self.texture = "svg/pieces/black_rook.svg"
        else:
            self.texture = "svg/pieces/white_rook.svg"

    def set_available_move(self, board: [Square], direction=None):
        if direction is None:
            direction = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            super().set_available_move(board, direction)

    def move(self, new_position, board: [Square]):
        super().move(new_position, board)
        self.moved = True

    def __str__(self):
        return "R"


class Bishop(Piece):

    def __init__(self, position, color):
        super().__init__(position, color)
        self.value = 50
        if color == BLACK:
            self.texture = "svg/pieces/black_bishop.svg"
        else:
            self.texture = "svg/pieces/white_bishop.svg"

    def set_available_move(self, board: [Square], direction=None):
        if direction is None:
            direction = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        super().set_available_move(board, direction)

    def __str__(self):
        return "B"


class King(Piece):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.value = 900
        self.moved = False
        self.castle = set()
        if color == BLACK:
            self.texture = "svg/pieces/black_king.svg"
        else:
            self.texture = "svg/pieces/white_king.svg"

    def set_available_move(self, board: [Square], directions=None):
        for square in [(line, column) for line in range(self.line - 1, self.line + 2) for column in
                       range(self.column - 1, self.column + 2) if 0 <= line < 8 and 0 <= column < 8 if not (
                    line == self.line and column == self.column)]:
            if board[square[0]][square[1]].piece is None:
                if len(board[square[0]][square[1]].attack.values()) == \
                        len([values for values in board[square[0]][square[1]].attack.values() if values == self.color]):
                    self.attack[square] = ()
            else:
                if board[square[0]][square[1]].piece.color != self.color:
                    if len(board[square[0]][square[1]].counterattack) == 0:
                        self.attack[square] = square
                else:
                    self.counterattack.append(square)
        if not self.moved:
            for dir_x in [1, -1]:
                x = self.column + dir_x
                OUT = True
                while x != 0 and x != 7:
                    if board[self.line][x].piece is not None or \
                            len([x for x in board[self.line][x].attack.values() if x != self.color]) != 0:
                        OUT = False
                    x += dir_x
                if OUT and board[self.line][x].piece is not None\
                        and isinstance(board[self.line][x].piece, Rook) \
                        and not board[self.line][x].piece.moved:
                    self.castle.add((self.line, x))
                else:
                    self.castle.discard((self.line, x))

    def move(self, new_position, board: [Square]):
        super().move(new_position, board)
        self.moved = True
        self.castle = set()

    def __str__(self):
        return "K"


class Queen(Rook, Bishop):
    def __init__(self, position, color):
        super().__init__(position, color)
        self.value = 90
        if color == BLACK:
            self.texture = "svg/pieces/black_queen.svg"
        else:
            self.texture = "svg/pieces/white_queen.svg"

    def set_available_move(self, board: [Square], direction=None):
        Rook.set_available_move(self, board)
        Bishop.set_available_move(self, board)

    def __str__(self):
        return "Q"


if __name__ == "__main__":
    pc = 9
    print(-pc)
