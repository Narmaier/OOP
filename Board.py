import numpy as np

from Pieces import *
from Player import Player
from Square import *


class Board:
    PIECES_ORDER = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    def __init__(self):
        self.board = np.array([[Square(None) for _ in range(8)] for _ in range(8)])
        self.kings = []
        self.white_pieces = []
        self.black_pieces = []

    def fill_board(self):
        for i in range(8):
            self.board[0][i].change_piece(self.PIECES_ORDER[i]((0, i), BLACK))
            self.board[1][i].change_piece(Pawn((1, i), BLACK))
            self.board[7][i].change_piece(self.PIECES_ORDER[i]((7, i), WHITE))
            self.board[6][i].change_piece(Pawn((6, i), WHITE))
        self.kings.append(self.pieceAt((7, 4)))
        self.kings.append(self.pieceAt((0, 4)))
        self.fill_pieces_lists()

    def fill_pieces_lists(self):
        for i in range(8):
            for j in range(8):
                item = self.pieceAt((i, j))
                if item is not None:
                    if item.color == BLACK:
                        self.black_pieces.append(item)
                    else:
                        self.white_pieces.append(item)

    def get_pieces_list(self, player):
        if player.side == BLACK:
            return self.black_pieces
        else:
            return self.white_pieces

    def clean_board(self):
        for i in range(8):
            for j in range(8):
                self.board[i][j].delete_piece()

    def pieceAt(self, position):
        return self.board[position[0]][position[1]].piece

    def get_king(self, player):
        if player.side == BLACK:
            return self.kings[1]
        else:
            return self.kings[0]

    def per_update_stats(self):
        for i in [0, 1, 6, 7]:
            for j in range(8):
                self.board[i][j].piece.set_available_move(self.board)
                self.add_stats((i, j))

    def add_stats(self, position):
        if isinstance(self.board[position[0]][position[1]].piece, Pawn):
            direction = self.board[position[0]][position[1]].piece.direction
            if 0 <= position[0] + direction < 8:
                for column in [column for column in [position[1] - 1, position[1] + 1] if 0 <= column < 8]:
                    self.board[position[0] + direction][column].attack[position] = \
                        self.board[position[0]][position[1]].piece.color
        else:
            for attack in [keys for keys, values in self.board[position[0]][position[1]].piece.attack.items()]:
                self.board[attack[0]][attack[1]].attack[position] = self.board[position[0]][position[1]].piece.color
        for counterattack in self.board[position[0]][position[1]].piece.counterattack:
            self.board[counterattack[0]][counterattack[1]].counterattack.append(position)

    def delete_stats(self, position):
        if isinstance(self.board[position[0]][position[1]].piece, Pawn):
            direction = self.board[position[0]][position[1]].piece.direction
            if 0 <= position[0] + direction < 8:
                for column in [column for column in [position[1] - 1, position[1] + 1] if 0 <= column < 8]:
                    self.board[position[0] + direction][column].attack.pop(position, None)
        else:
            for attack in [keys for keys in self.board[position[0]][position[1]].piece.attack.keys()]:
                self.board[attack[0]][attack[1]].attack.pop(position, None)
        for counterattack in self.board[position[0]][position[1]].piece.counterattack:
            if position in self.board[counterattack[0]][counterattack[1]].counterattack:
                self.board[counterattack[0]][counterattack[1]].counterattack.remove(position)

    def attack_piece(self, player: Player, new_position):
        new_line, new_column = new_position
        self.delete_stats(new_position)
        player.add_piece(self.board[new_line][new_column].piece)
        self.board[new_line][new_column].delete_piece()

    def replace_piece(self, position, new_position):
        new_line, new_column = new_position
        line, column = position
        self.delete_stats(position)
        self.board[new_line][new_column].change_piece(self.board[line][column].piece)
        self.board[line][column].piece.move(new_position, self.board)
        self.board[line][column].delete_piece()
        self.add_stats(new_position)
        self.update_squares_stats(position)
        self.update_squares_stats(new_position)

    def move_piece(self, position, new_position, player: Player):
        line, column = position
        if self.board[line][column].piece is not None:
            state = self.board[line][column].piece.check_move(new_position)
            if state is not None:
                attack = self.board[line][column].piece.attack[new_position]
                if state:
                    self.attack_piece(player, attack)
                    self.replace_piece(position, new_position)
                else:
                    self.replace_piece(position, new_position)
                return attack
            else:
                return None
        else:
            return None

    def long_castling(self, king):
        self.replace_piece((king.line, 4), (king.line, 2))
        self.replace_piece((king.line, 0), (king.line, 3))

    def short_castling(self, king):
        self.replace_piece((king.line, 4), (king.line, 6))
        self.replace_piece((king.line, 7), (king.line, 5))

    def castle_move(self, position, new_position):
        if isinstance(self.pieceAt(position), King) and isinstance(self.pieceAt(new_position), Rook):
            if self.pieceAt(position) and self.pieceAt(new_position):
                x_direction = (new_position[1] - position[1])
                castle_available = True
                buf_x = position[1] + x_direction
                while buf_x != new_position[1]:
                    if self.pieceAt((position[0],buf_x)) is not None:
                        castle_available = False
                        break
                if castle_available:
                    pass
        else:
            return False


    def sub_up_function(self, square):
        self.delete_stats(square)
        self.board[square[0]][square[1]].piece.clear_statements()
        self.board[square[0]][square[1]].piece.set_available_move(self.board)
        self.add_stats(square)

    def update_kings(self):
        for _ in range(2):
            king = self.kings[_]
            square = king.line, king.column
            self.sub_up_function(square)

    def update_squares_stats(self, position):
        for square in [(line + position[0], column + position[1]) for line in [-2, -1, 1, 2] for column in
                       [-2, -1, 1, 2]
                       if abs(line) != abs(column) if 0 <= line + position[0] < 8 if 0 <= column + position[1] < 8]:
            if self.board[square[0]][square[1]].piece is not None:
                self.sub_up_function(square)
        for direction in [(-1, 0), (0, -1), (0, 1), (1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
            line, column = position
            while 0 <= line + direction[0] < 8 and 0 <= column + direction[1] < 8:
                line += direction[0]
                column += direction[1]
                if self.board[line][column].piece is not None:
                    break
            if 0 <= line < 8 and 0 <= column < 8 and self.board[line][column].piece is not None:
                self.sub_up_function((line, column))
        self.update_kings()

    def display_board(self):
        for i in range(8):
            buf_str = ""
            for j in range(8):
                buf_str += "[" + str(self.board[i][j]) + "]"
                if buf_str == None:
                    print(1)
            print(buf_str)

    def display_piece(self):
        for i in range(8):
            buf = []
            for j in range(8):
                buf.append(len(self.board[i][j].pawn_moves))
            print(buf)

    def display_attacks(self):
        for i in range(8):
            buf = []
            for j in range(8):
                buf.append(len(self.board[i][j].attack))
            print(buf)

    # def get_moves(self, side):
    #     buffer = []
    #     for i in range(8):
    #         for j in range(8):
    #             for move in self.get_piece_attack_keys(i, j):
    #                 if self.board[i][j].piece.color == side:
    #                     buffer.append(((i, j), move))
    #     return buffer
    #
    # def get_piece_attack_keys(self, x, y):
    #     if self.board[x][y].piece is None:
    #         return ()
    #     else:
    #         return self.board[x][y].piece.attack


if __name__ == "__main__":
    board = Board()
    board.fill_board()
    board.per_update_stats()

