import sys
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import (
    QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView, QMainWindow, QGraphicsItemGroup, QWidget)
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, QPointF, QRectF
from PyQt5.QtSvg import QGraphicsSvgItem
from stockfish import Stockfish
from StartMenu import Result
from Promotions import Promotion
from Board import Board, WHITE, BLACK
from Game import Game
from Pieces import King, Pawn
import time


class BotThread(QThread):
    turn_changed = pyqtSignal(QGraphicsSvgItem, QPointF)
    piece_deleted = pyqtSignal(QGraphicsSvgItem)
    promoted = pyqtSignal(int, int, str, str, str)

    def __init__(self, widget):
        super().__init__()
        self.side = None
        self.turn = True
        self.game = True
        self.widget = widget
        self.widget.turn.connect(self.change_turn)
        self.bot = Stockfish("D:/stockfish_15.1_win_x64_avx2/stockfish-windows-2022-x86-64-avx2", depth=16)

    def set_up_side(self, side):
        self.side = (side == WHITE)

    def stop(self):
        self.game = False

    def run(self):
        while self.game:
            # time.sleep()
            if self.turn == self.side:
                st = self.widget.game.oder_to_fen()
                self.bot.set_fen_position(st)
                move = self.bot.get_best_move()
                if move is None:
                    self.stop()
                    self.widget.game_status.emit(0)
                    continue
                if self.piece_action(move) or self.castling(move):
                    self.turn = not self.turn
                    self.widget.turn.emit(self.turn)
                if len(move) == 5:
                    position = self.widget.game.tuple_move(move)[1]
                    self.promote(position, move[4])
                if self.widget.game.game_status is not None:
                    self.stop()
                    self.widget.game_status.emit(self.widget.game.game_status)

    def move_animation(self, item, position):
        current_position = item.pos()
        buf_position = current_position
        X_direction = (position.x() - current_position.x())//9
        Y_direction = (position.y() - current_position.y())//9

        for _ in range(9):
            time.sleep(0.01)
            buf_position.setX(buf_position.x() + X_direction)
            buf_position.setY(buf_position.y() + Y_direction)
            self.turn_changed.emit(item, buf_position)

    def castling_move_animation(self, king, rook, king_pos, rook_pos):
        current_king_pos = king.pos()
        current_rook_pos = rook.pos()

        king_buff = current_king_pos
        rook_buff = current_rook_pos

        XKing_direction = (king_pos.x() - current_king_pos.x())//9
        XRook_direction = (rook_pos.x() - current_rook_pos.x())//9

        for _ in range(9):
            time.sleep(0.01)
            king_buff.setX(king_buff.x() + XKing_direction)
            self.turn_changed.emit(king, king_buff)
            rook_buff.setX(rook_buff.x() + XRook_direction)
            self.turn_changed.emit(rook, rook_buff)

    def piece_action(self, move):
        position = self.widget.game.tuple_move(move)
        state = self.widget.game.round(position[0], position[1])
        if state is not None:
            remove_item = None
            item = self.widget.scene.itemAt(position[0][1] * 72 + 9, position[0][0] * 72 + 9, QTransform())
            self.widget.piece_moved.emit(move)
            if state != ():
                remove_item = self.widget.scene.itemAt(state[1] * 72 + 36, state[0] * 72 + 36, QTransform())
                self.widget.piece_taken.emit(self.turn)
            self.move_animation(item, QPointF(position[1][1] * 72 + 9, position[1][0] * 72 + 9))
            self.delete_piece(remove_item)
            return True
        return False

    def castling(self, move):
        position = self.widget.game.tuple_move(move)
        if isinstance(self.widget.game.board.pieceAt(position[0]), King):
            king = self.widget.game.board.pieceAt(position[0])
            self.widget.game.update_castling_fen(king)
            pos = self.widget.toScene_coordinate(position[0])
            svg_king = self.widget.scene.itemAt(pos, QTransform())
            self.widget.game.rounds += 1
            if position[0][1] - position[1][1] > 0:
                self.widget.game.board.long_castling(king)
                pos = self.widget.toScene_coordinate((king.line, 0))
                svg_rook = self.widget.scene.itemAt(pos, QTransform())
                self.castling_move_animation(svg_king, svg_rook,
                                             self.widget.toScene_coordinate((king.line, 2)),
                                             self.widget.toScene_coordinate((king.line, 3)))
            else:
                self.widget.game.board.short_castling(king)
                pos = self.widget.toScene_coordinate((king.line, 7))
                svg_rook = self.widget.scene.itemAt(pos, QTransform())
                self.castling_move_animation(svg_king, svg_rook,
                                             self.widget.toScene_coordinate((king.line, 6)),
                                             self.widget.toScene_coordinate((king.line, 5)))
            return True
        return False

    def delete_piece(self, item):
        if item is not None:
            self.piece_deleted.emit(item)

    @pyqtSlot(bool)
    def change_turn(self, turn):
        self.turn = turn

    def promote(self, position, promote_index):
        index = {"q": "queen", "n": "knight", "r": "rook", "b": "bishop"}
        if self.side:
            side = "white"
        else:
            side = "black"
        path = f"svg/pieces/{side}_{index[promote_index]}.svg"
        color = self.widget.game.board.pieceAt(position).color
        self.promoted.emit(position[0], position[1], path, color, promote_index)


class ChessPiece(QGraphicsSvgItem):
    moved = pyqtSignal(QGraphicsSvgItem)
    pressed = pyqtSignal(QGraphicsSvgItem)

    def __init__(self, turn, texture):
        super().__init__(texture)
        self.oldPos = None
        self.turn = (turn == WHITE)

    def mousePressEvent(self, event):
        self.setZValue(10)
        self.oldPos = self.pos()
        self.pressed.emit(self)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            rect = self.scene().sceneRect()
            if not rect.contains(value):
                value.setX(min(rect.right(), max(value.x(), rect.left())))
                value.setY(min(rect.bottom(), max(value.y(), rect.top())))
                return value
        return QGraphicsItem.itemChange(self, change, value)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        x, y = self.pos().x(), self.pos().y()
        self.setPos(((x + 26) // 72) * 72 + 9, ((y + 26) // 72) * 72 + 9)
        self.moved.emit(self)

    def get_turn(self):
        return self.turn

    def get_oldPos(self):
        return self.oldPos

    @pyqtSlot(bool)
    def check_turn(self, turn):
        white_or_black = (turn == self.turn)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            enabled=white_or_black)


class BoardWidget(QGraphicsView):
    turn = pyqtSignal(bool)
    piece_taken = pyqtSignal(bool)
    game_status = pyqtSignal(int)
    piece_moved = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.bot_side = None
        self.board = None
        self.game = None
        self._current_turn = None
        self.view = None
        self.scene = None
        self._availableMoveGroup = None
        self.promote_widget = None
        self.start_game()
        # self.view = QGraphicsView()
        # self.view.setScene(self.scene)
        # self.view.setSceneRect(0, 0, 576, 576)

    def start_game(self, bot_side=None):
        if bot_side is None:
            self.versus()
        else:
            self.versus_bot(bot_side)

    @pyqtSlot()
    def pot_promote(self):
        pass

    def versus(self):
        self.scene = QGraphicsScene()
        self._current_turn = True
        board = QGraphicsSvgItem("svg/Board1.svg")
        board.setZValue(-10)
        self.scene.addItem(board)
        self.game = Game()
        self.board = self.game.get_board()
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j].piece is not None:
                    turn, texture = self.board.board[i][j].piece.color, self.board.board[i][j].piece.texture
                    svg_item = ChessPiece(turn, texture)
                    svg_item.setScale(0.75)
                    svg_item.setPos(j * 72 + 9, i * 72 + 9)
                    svg_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsToShape)
                    if turn == WHITE:
                        svg_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
                    self.turn.connect(svg_item.check_turn)
                    svg_item.moved.connect(self.toggle_turn)
                    svg_item.pressed.connect(self.fill_available_move_group)
                    svg_item.moved.connect(self.remove_available_move_group)
                    self.scene.addItem(svg_item)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 576, 576)

    @pyqtSlot(bool)
    def change_turn(self, turn):
        self._current_turn = turn

    def versus_bot(self, bot_side):
        self.scene = QGraphicsScene()
        self._current_turn = (bot_side != WHITE)
        board = QGraphicsSvgItem("svg/Board1.svg")
        board.setZValue(-10)
        self.scene.addItem(board)
        self.game = Game()
        self.bot = BotThread(self)
        self.bot.turn_changed.connect(self.change_piece_position)
        self.bot.piece_deleted.connect(self.delete_piece)
        self.bot.promoted.connect(self.promote)
        self.board = self.game.get_board()
        self.bot.set_up_side(bot_side)
        self.turn.connect(self.change_turn)
        self.bot.start()
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j].piece is not None:
                    turn, texture = self.board.board[i][j].piece.color, self.board.board[i][j].piece.texture
                    svg_item = ChessPiece(turn, texture)
                    svg_item.setScale(0.75)
                    svg_item.setPos(j * 72 + 9, i * 72 + 9)
                    svg_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsToShape)
                    if turn != bot_side:
                        svg_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, enabled=self._current_turn)
                        svg_item.moved.connect(self.toggle_turn)
                        self.turn.connect(svg_item.check_turn)
                    svg_item.pressed.connect(self.fill_available_move_group)
                    svg_item.moved.connect(self.remove_available_move_group)
                    self.scene.addItem(svg_item)
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 576, 576)

    @pyqtSlot(QGraphicsSvgItem, QPointF)
    def change_piece_position(self, a0, a1):
        a0.setPos(a1)

    @pyqtSlot(QGraphicsSvgItem)
    def delete_piece(self, item):
        self.scene.removeItem(item)

    def get_taken_pieces(self, index):
        return self.game.players[index].taken_pieces

    def get_win_side(self):
        return self.game.get_winner_side()

    def toBoard_coordinate(self, x, y):
        return int(x // 72), int(y // 72)

    def toScene_coordinate(self, position):
        return QPointF(position[1] * 72 + 9, position[0] * 72 + 9)

    def isPromote(self, position):
        return isinstance(self.game.board.pieceAt(position), Pawn) and (position[0] == 0 or position[0] == 7)

    def show_promote_widget(self, position, side):
        if side == BLACK:
            self.promote_widget = Promotion(BLACK, position, self.parent())
        else:
            self.promote_widget = Promotion(WHITE, position, self.parent())
        self.promote_widget.promoted.connect(self.promote)
        self.promote_widget.show()

    @pyqtSlot(int, int, str, str, str)
    def promote(self, x, y, path, side, promote_index):
        self.game.promote((x, y), promote_index)
        pos = self.toScene_coordinate((x, y))
        self.scene.removeItem(self.scene.itemAt(pos, QTransform()))
        svg_item = ChessPiece(side, path)
        svg_item.setScale(0.75)
        svg_item.setPos(pos)
        self.turn.connect(svg_item.check_turn)
        svg_item.moved.connect(self.toggle_turn)
        svg_item.pressed.connect(self.fill_available_move_group)
        svg_item.moved.connect(self.remove_available_move_group)
        self.scene.addItem(svg_item)
        self.updateSceneRect(QRectF(0, 0, 576, 576))
        if self.promote_widget is not None:
            self.promote_widget.hide()

    def piece_action(self, item):
        y, x = self.toBoard_coordinate(item.get_oldPos().x(), item.get_oldPos().y())
        new_y, new_x = self.toBoard_coordinate(item.pos().x(), item.pos().y())
        piece = self.board.pieceAt((x, y))
        position = self.game.round((x, y), (new_x, new_y))
        item.setZValue(-1)
        if position is not None:
            if self.isPromote((new_x, new_y)):
                self.show_promote_widget((new_x, new_y), piece.color)
                print((new_x, new_y))
            if position != ():
                self.piece_taken.emit(self._current_turn)
                self.scene.removeItem(self.scene.itemAt(self.toScene_coordinate(position), QTransform()))
            item.setZValue(0)
            self._current_turn = not self._current_turn
            self.turn.emit(self._current_turn)
            self.piece_moved.emit(f"{self.game.move_to_str((x,y))}{self.game.move_to_str((new_x,new_y))}")
            return True
        return False

    def castling(self, king):
        y, x = self.toBoard_coordinate(king.get_oldPos().x(), king.get_oldPos().y())
        new_x, new_y = self.toBoard_coordinate(king.pos().x(), king.pos().y())
        rook = self.scene.itemAt(self.toScene_coordinate((new_y, new_x)), QTransform())
        state = self.game.castling_move((x, y), (new_y, new_x))
        if state is not None:
            self._current_turn = not self._current_turn
            self.turn.emit(self._current_turn)
        match state:
            case Game.SHORT_CASTLING:
                king.setPos(self.toScene_coordinate((x, 6)))
                rook.setPos(self.toScene_coordinate((x, 5)))
                self.piece_moved.emit("O-O")
                return True
            case Game.LONG_CASTLING:
                king.setPos(self.toScene_coordinate((x, 2)))
                rook.setPos(self.toScene_coordinate((x, 3)))
                self.piece_moved.emit("O-O-O")
                return True
            case _:
                return False

    @pyqtSlot(QGraphicsSvgItem)
    def toggle_turn(self, item):
        if self._current_turn == item.get_turn():
            if self.piece_action(item) or self.castling(item):
                if self.game.game_status is not None:
                    self.game_status.emit(self.game.game_status)
            else:
                item.setPos(item.get_oldPos())

    @pyqtSlot(QGraphicsSvgItem)
    def fill_available_move_group(self, item):
        board = self.game.get_board()
        self._availableMoveGroup = QGraphicsItemGroup()
        y, x = int(item.get_oldPos().x() // 72), int(item.get_oldPos().y() // 72)
        for key, value in board.board[x][y].piece.attack.items():
            if board.board[x][y].piece.attack[key] == ():
                point = QGraphicsSvgItem("svg/point.svg")
                point.setPos(key[1] * 72, key[0] * 72)
            else:
                point = QGraphicsSvgItem("svg/square.svg")
                point.setPos(value[1] * 72, value[0] * 72)
            self._availableMoveGroup.addToGroup(point)
        self._availableMoveGroup.setZValue(-2)
        self.scene.addItem(self._availableMoveGroup)

    def remove_available_move_group(self):
        self.scene.removeItem(self._availableMoveGroup)


if __name__ == "__main__":
    app_instance = QApplication(sys.argv)

    main_window = BoardWidget()
    main_window.show()

    app_instance.exec()
