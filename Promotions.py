from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTime, QPointF
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QButtonGroup
from Square import BLACK, WHITE
from UIs.promotionsUI import Ui_Form as PromotionUI
from Pieces import Queen, Knight, Rook, Bishop
from PyQt5 import QtCore


class Promotion(QWidget, PromotionUI):
    promoted = pyqtSignal(int, int, str, str, str)

    def __init__(self, side, pos, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.side = side
        self.pos = pos
        if side == BLACK:
            self.setBlack()
        else:
            self.setWhite()
        self.pushButton.pressed.connect(self.promoteToQueen)
        self.pushButton_2.pressed.connect(self.promoteToRook)
        self.pushButton_3.pressed.connect(self.promoteToBishop)
        self.pushButton_4.pressed.connect(self.promoteToKnight)

    def setBlack(self):
        self.pushButton.setIcon(QIcon(QPixmap("svg/pieces/black_queen.svg")))
        self.pushButton_2.setIcon(QIcon(QPixmap("svg/pieces/black_rook.svg")))
        self.pushButton_3.setIcon(QIcon(QPixmap("svg/pieces/black_bishop.svg")))
        self.pushButton_4.setIcon(QIcon(QPixmap("svg/pieces/black_knight.svg")))

    def setWhite(self):
        self.pushButton.setIcon(QIcon(QPixmap("svg/pieces/white_queen.svg")))
        self.pushButton_2.setIcon(QIcon(QPixmap("svg/pieces/white_rook.svg")))
        self.pushButton_3.setIcon(QIcon(QPixmap("svg/pieces/white_bishop.svg")))
        self.pushButton_4.setIcon(QIcon(QPixmap("svg/pieces/white_knight.svg")))

    def promoteToQueen(self):
        if self.side == BLACK:
            item_path = "svg/pieces/black_queen.svg"
        else:
            item_path = "svg/pieces/white_queen.svg"
        self.promoted.emit(self.pos[0], self.pos[1], item_path, self.side, "q")

    def promoteToKnight(self):
        if self.side == BLACK:
            item_path = "svg/pieces/black_knight.svg"
        else:
            item_path = "svg/pieces/white_knight.svg"
        self.promoted.emit(self.pos[0], self.pos[1], item_path, self.side, "n")

    def promoteToRook(self):
        if self.side == BLACK:
            item_path = "svg/pieces/black_rook.svg"
        else:
            item_path = "svg/pieces/white_rook.svg"
        self.promoted.emit(self.pos[0], self.pos[1], item_path, self.side, "r")

    def promoteToBishop(self):
        if self.side == BLACK:
            item_path = "svg/pieces/black_bishop.svg"
        else:
            item_path = "svg/pieces/white_bishop.svg"
        self.promoted.emit(self.pos[0], self.pos[1], item_path, self.side, "b")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = Promotion(WHITE)
    widget.show()
    sys.exit(app.exec_())
