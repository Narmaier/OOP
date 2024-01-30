from Player import Player, ChessBot
from Board import Board, WHITE, BLACK
from Pieces import *
import copy
from stockfish import Stockfish
import time

WIN = 1
STANDOFF = 0


class Game:
    LONG_CASTLING = 0
    SHORT_CASTLING = 1

    def __init__(self):
        self.castling = None
        self.pawn_move = None
        self.winner = None
        self.board = Board()
        self.board.fill_board()
        self.board.per_update_stats()
        self.rounds = None
        self.current_round = None
        self.stalemate = None
        self.players = None
        self.game_status = None
        self.clear()

    def clear(self):
        self.board = Board()
        self.board.fill_board()
        self.board.per_update_stats()
        self.rounds = 0
        self.stalemate = 0
        self.castling = "KQkq"
        self.current_round = 0
        self.pawn_move = "-"
        self.game_status = None
        self.winner = None
        self.players = [Player("player_1", WHITE), Player("player_2", BLACK)]

    def check_game_status(self):
        return self.game_status

    def get_winner_side(self):
        return self.winner.side

    def get_board(self):
        return self.board

    def check_standoff(self):
        if self.stalemate >= 10:
            self.game_status = STANDOFF

    def checkmate(self, player):
        state = True
        OUT = False
        if self.check_king(self.board.get_king(player), self.board):
            pieces_list = self.board.get_pieces_list(player)
            for piece in pieces_list:
                for move in piece.attack.keys():
                    if self.checkIsSolved(piece.pos(), move):
                        state = False
                        OUT = True
                        break
                if OUT:
                    break
            if state:
                self.game_status = WIN
                self.winner = self.players[(self.rounds + 1) % 2]

    def check_king(self, king, board):
        line, column = king.line, king.column
        side = king.color
        return len([value for value in board.board[line][column].attack.values() if value != side]) > 0

    def checkIsSolved(self, position, new_position):
        buf_player = copy.deepcopy(self.players[self.rounds % 2])
        buf_board = copy.deepcopy(self.board)
        buf_board.move_piece(position, new_position, buf_player)
        return not self.check_king(buf_board.get_king(buf_player), buf_board)

    def move_try(self, position, new_position):
        state = self.board.move_piece(position, new_position, self.players[self.rounds % 2])
        if state is not None:
            if self.rounds % 2 == 0:
                self.current_round += 1
            self.rounds += 1
            self.checkmate(self.players[self.rounds % 2])
            self.update_stalemate(new_position, state)
            if isinstance(self.board.pieceAt(new_position), King):
                self.update_castling_fen(self.board.pieceAt(new_position))
        return state

    def promote(self, position, promote_index):
        item = self.board.pieceAt(position)
        match promote_index:
            case "q":
                item.promote(Queen, position, item.color)
            case "r":
                item.promote(Rook, position, item.color)
            case "b":
                item.promote(Bishop, position, item.color)
            case "n":
                item.promote(Knight, position, item.color)
        item.set_available_move(self.board.board)

    def check_castling_available(self, king, rook):
        new_position = rook.pos()
        king_pos = king.pos()
        if king.color == rook.color and new_position in king.castle and not self.check_king(king, self.board):
            direction = (new_position[1] - king_pos[1])//abs(new_position[1] - king_pos[1])
            side = king.color
            OUT = True
            for _ in range(2):
                if len([value for value in self.board.board[king_pos[0]][king_pos[1]+direction].attack.values()
                        if value != side]) > 0:
                    OUT = False
                    break
            return OUT
        else:
            return False

    def castling_move(self, position, new_position):
        king = self.board.pieceAt(position)
        rook = self.board.pieceAt(new_position)
        if isinstance(king, King) and (rook, Rook):
            if self.check_castling_available(king, rook):
                self.rounds += 1
                if new_position[1] - position[1] == 3:
                    self.board.short_castling(king)
                    return Game.SHORT_CASTLING
                else:
                    self.board.long_castling(king)
                    return Game.LONG_CASTLING
        return None

    def round(self, position, new_position):
        if self.check_king(self.board.get_king(self.players[self.rounds % 2]), self.board):
            if self.checkIsSolved(position, new_position):
                return self.move_try(position, new_position)
            else:
                return None
        else:
            return self.move_try(position, new_position)

    def move_to_str(self, position):
        letter_values = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

        return letter_values[position[1]] + str(8 - position[0])

    def update_stalemate(self, position, state):
        self.pawn_move = "-"
        piece = self.board.board[position[0]][position[1]].piece
        if isinstance(piece, Pawn):
            if piece.double_move:
                self.pawn_move = self.move_to_str((position[0] - piece.direction, position[1]))
        else:
            if state == ():
                self.stalemate += 1

    def update_castling_fen(self, piece):
        if piece.color == BLACK:
            self.castling = self.castling.replace("kq", "")
        else:
            self.castling = self.castling.replace("KQ", "")

    def oder_to_fen(self):
        fen = ""
        fun = lambda x: str(x) if x != 0 else ""
        for i in range(8):
            buf_fen = ""
            value = 0
            for j in range(8):
                buf = str(self.board.board[i][j])
                if buf == "*":
                    value += 1
                else:
                    buf_fen += fun(value) + buf
                    value = 0
            fen += buf_fen + fun(value) + "/"

        if self.rounds % 2 == 0:
            fen = f"{fen[:-1]} w {self.castling} {self.pawn_move} {self.stalemate} {self.rounds}"
        else:
            fen = f"{fen[:-1]} b {self.castling} {self.pawn_move} {self.stalemate} {self.rounds}"
        return fen

    def tuple_move(self, str_move):
        letter_values = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        move = (8 - int(str_move[1]), letter_values[str_move[0]])
        new_move = (8 - int(str_move[3]), letter_values[str_move[2]])
        return move, new_move


if __name__ == "__main__":
    game = Game()
    game.round((1, 7), (3, 7))
    bot = Stockfish("D:/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2")
    bot.set_fen_position("6nr/5Ppk/7p/8/8/8/8/6K1 w - 4 12")
    print(bot.get_best_move())
