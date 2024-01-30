import numba.core.types

from Square import *
from Pieces import Piece
import copy
from numba.core.types import pyobject, int32, string
from numba.experimental import jitclass
import numpy as np
from threading import Thread

class Player:
    # win_player = None

    def __init__(self, name=None, side=None):
        self.name = name
        self.side = side
        self.taken_pieces: [Piece] = []
        self.king_position = None
        if side == BLACK:
            self.king_position = (0, 4)
        elif side == WHITE:
            self.king_position = (7, 4)

    def set_name(self, new_name):
        self.name = new_name

    def set_side(self, new_side):
        self.side = new_side
        if new_side == BLACK:
            self.king_position = (0, 4)
        else:
            self.king_position = (7, 4)

    def add_piece(self, piece):
        self.taken_pieces.append(piece)

    def change_king_position(self, new_position):
        self.king_position = new_position

    def clean_pieces(self):
        self.taken_pieces = []

    def fill_solve_moves(self, array):
        self.solve_moves = array

    # @classmethod
    # def winner(cls, self):
    #     cls.win_player = self
    #
    # def win(self):
    #     Player.winner(self)


spec = [('side', string)]


# @jitclass(spec)
class ChessBot:
    def __init__(self, side):
        self.side = side
        self.values = []

    def best_move(self, game, depth, isMaximising):
        self.values = []
        for move in game.get_moves(self.side):
            buffer_game = copy.deepcopy(game)
            buffer_game.move_piece(move[0], move[1], Player())
            # value = self.minimax(depth - 1, buffer_game, -10000, 10000, not isMaximising)
            thread = Thread(target=self.test, args=(depth - 1, buffer_game, -10000, 10000, not isMaximising, move,))
            thread.start()
        return sorted(self.values, reverse=True)[0][0]

    def test(self, depth, game, alpha, beta, is_maximising, move):
        value = self.minimax(depth, game, alpha, beta, is_maximising)
        self.values.append((move, value))

    def minimax(self, depth, game, alpha, beta, is_maximising):
        if depth == 0:
            return -np.sum([x.value for x in game.board.ravel()])
        if is_maximising:
            best_move_value = -9999
            for move in game.get_moves(self.side):
                buffer_game = copy.deepcopy(game)
                buffer_game.move_piece(move[0], move[1], Player())
                best_move_value = np.max(np.array([best_move_value,
                                                   self.minimax(depth - 1, buffer_game, alpha, beta,
                                                                not is_maximising)]))
                alpha = np.max(np.array([alpha, best_move_value]))
                if beta <= alpha:
                    return best_move_value
            return best_move_value
        else:
            best_move_value = 9999
            for move in game.get_moves(self.side):
                buffer_game = copy.deepcopy(game)
                buffer_game.move_piece(move[0], move[1], Player())
                best_move_value = np.min(np.array([best_move_value,
                                                   self.minimax(depth - 1, buffer_game, alpha, beta,
                                                                not is_maximising)]))
                beta = np.min(np.array([beta, best_move_value]))
                if beta <= alpha:
                    return best_move_value
            return best_move_value

    def piece_value(self, piece):
        match piece:
            case "K":
                value = 900
            case "Q":
                value = 90
            case "R":
                value = 50
            case "B":
                value = 30
            case "H":
                value = 30
            case "P":
                value = 10
            case _:
                value = 0
        return value

    def evaluate_board(self, board):
        value = 0
        for line in board:
            for square in line:
                value += self.piece_value(str(square.piece))
        return value
