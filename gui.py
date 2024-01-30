import sys
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import (
    QApplication, QGraphicsItem, QGraphicsScene, QGraphicsView, QMainWindow)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtSvg import QGraphicsSvgItem


class ChessPiece(QGraphicsSvgItem):
    moved = pyqtSignal(QGraphicsSvgItem)

    def __init__(self, index):
        super().__init__(self.svg)
        self.oldPos = None
        self.index = index

    def mousePressEvent(self, event):
        self.oldPos = self.pos()
        self.setZValue(10)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            rect = self.scene().sceneRect()
            if not rect.contains(value):
                # Keep the item inside the scene rect.
                value.setX(min(rect.right(), max(value.x(), rect.left())))
                value.setY(min(rect.bottom(), max(value.y(), rect.top())))
                return value
        return QGraphicsItem.itemChange(self, change, value)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        x, y = self.pos().x(), self.pos().y()
        self.setPos(((x+26)//72)*72 + 9, ((y+26)//72)*72 + 9)
        self.moved.emit(self)

    def get_turn(self):
        return self._turn

    @pyqtSlot(bool)
    def check_turn(self, turn):
        white_or_black = (turn == self._turn)
        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            enabled=white_or_black)


class WhitePawn(ChessPiece):
    _turn = True
    svg = "svg/pieces/white_pawn.svg"


class WhiteRook(ChessPiece):
    _turn = True
    svg = "svg/pieces/white_rook.svg"


class WhiteKnight(ChessPiece):
    _turn = True
    svg = "svg/pieces/white_knight.svg"


class WhiteBishop(ChessPiece):
    _turn = True
    svg = "svg/pieces/white_bishop.svg"


class WhiteQueen(ChessPiece):
    _turn = True
    svg = "svg/pieces/white_queen.svg"


class WhiteKing(ChessPiece):
    _turn = True
    svg = "svg/pieces/white_king.svg"


class BlackPawn(ChessPiece):
    _turn = False
    svg = "svg/pieces/black_pawn.svg"


class BlackRook(ChessPiece):
    _turn = False
    svg = "svg/pieces/black_rook.svg"


class BlackKnight(ChessPiece):
    _turn = False
    svg = "svg/pieces/black_knight.svg"


class BlackBishop(ChessPiece):
    _turn = False
    svg = "svg/pieces/black_bishop.svg"


class BlackQueen(ChessPiece):
    _turn = False
    svg = "svg/pieces/black_queen.svg"


class BlackKing(ChessPiece):
    _turn = False
    svg = "svg/pieces/black_king.svg"


class MainWindow(QMainWindow):
    turn = pyqtSignal(bool)
    def __init__(self):
        super().__init__()

        self._current_turn = True

        self.scene = QGraphicsScene()
        board = QGraphicsSvgItem("svg/Board1.svg")
        self.scene.setSceneRect(0, 0, 522, 522)
        weight = 576
        height = 576
        buf_height = 9
        buf_weight = 0
        board.setZValue(-2)
        self.scene.addItem(board)
        w_direction = [WhiteRook, WhiteKnight, WhiteBishop, WhiteQueen, WhiteKing, WhiteBishop, WhiteKnight, WhiteRook]
        b_direction = [BlackRook, BlackKnight, BlackBishop, BlackQueen, BlackKing, BlackBishop, BlackKnight, BlackRook]
        self.ind = []
        for _ in range(8):
            _piece = w_direction[_](_)
            _piece.setScale(0.75)
            buf_weight += 9
            _piece.setPos(buf_weight, buf_height)
            _piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            _piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges)
            _piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsToShape)
            self.turn.connect(_piece.check_turn)
            _piece.moved.connect(self.toggle_turn)
            buf_weight += 63
            self.scene.addItem(_piece)
            self.ind.append(_piece)
        buf_weight = 0
        buf_height += height / 8
        for _ in range(8):
            piece = WhitePawn(_)
            piece.setScale(0.75)
            buf_weight += 9
            piece.setPos(buf_weight, buf_height)
            piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsToShape)
            self.turn.connect(piece.check_turn)
            piece.moved.connect(self.toggle_turn)
            buf_weight += 63
            self.scene.addItem(piece)
        buf_weight = 0
        buf_height += (height / 8)*5
        for _ in range(8):
            _piece = BlackPawn(_)
            _piece.setScale(0.75)
            buf_weight += 9
            _piece.setPos(buf_weight, buf_height)
            _piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsToShape)
            self.turn.connect(_piece.check_turn)
            _piece.moved.connect(self.toggle_turn)
            buf_weight += 63
            self.scene.addItem(_piece)
        buf_weight = 0
        buf_height += (height / 8)
        for _ in range(8):
            _piece = b_direction[_](_)
            _piece.setScale(0.75)
            buf_weight += 9
            _piece.setPos(buf_weight, buf_height)
            _piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            _piece.setFlag(QGraphicsItem.GraphicsItemFlag.ItemClipsToShape)
            self.turn.connect(_piece.check_turn)
            _piece.moved.connect(self.toggle_turn)
            buf_weight += 63
            self.scene.addItem(_piece)

        self.view = QGraphicsView()
        self.view.setScene(self.scene)
        self.view.setSceneRect(0, 0, 576, 576)
        self.setCentralWidget(self.view)

    @pyqtSlot(QGraphicsSvgItem)
    def toggle_turn(self, item):
        if self._current_turn == item.get_turn():
            item.setZValue(-1)
            self._current_turn = not self._current_turn
            if self.scene.itemAt(item.pos(), QTransform()) != item:
                self.scene.removeItem(self.scene.itemAt(item.pos(), QTransform()))
            item.setZValue(0)
            self.turn.emit(self._current_turn)



if __name__ == "__main__":
    app_instance = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    app_instance.exec()
