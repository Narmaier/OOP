import sys
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, QTime, QTimer, QRect, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from UIs.mainUI import Ui_MainWindow
from BoardWidget import BoardWidget
from TakenPiecesWidget import TakenPiecesWidget
from StartMenu import StartMenu, Result
from UIs.startUI import Ui_Form
from Game import WIN, STANDOFF
from Square import BLACK
from Promotions import Promotion


class GameWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parents=None):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.board_widget = BoardWidget(self.groupBox)
        self.board_widget.piece_taken.connect(self.update_taken_pieces)
        self.board_widget.game_status.connect(self.up_result)
        self.board_widget.setDisabled(True)

        self.white_pieces = TakenPiecesWidget(self.taken_white)
        self.black_pieces = TakenPiecesWidget(self.taken_black)
        self.timers = [QTimer(), QTimer()]
        self.times = [None, None]

        self.timers[0].timeout.connect(lambda: self.show_time(0))
        self.timers[1].timeout.connect(lambda: self.show_time(1))

        self.board_widget.turn.connect(self.timer_control)
        self.board_widget.piece_moved.connect(self.update_steps)

        self.result_widget = Result("ok", self)
        self.result_widget.setGeometry(QtCore.QRect(383 - 200, 380 - 150, 400, 300))
        self.result_widget.pushButton.pressed.connect(self.up_start)

        self.start_widget = StartMenu(self)
        self.start_widget.setGeometry(QtCore.QRect(383 - 200, 380 - 150, 400, 300))
        self.start_widget.pushButton.pressed.connect(self.start)

        self.result_widget.hide()

    def stop_timers(self):
        self.timers[0].stop()
        self.timers[1].stop()

    @pyqtSlot(int)
    def up_result(self, status):
        self.stop_timers()
        self.board_widget.setDisabled(True)

        if status == WIN:
            match self.board_widget.get_win_side():
                case "B":
                    self.result_widget.label.setText("Black wins")
                case "W":
                    self.result_widget.label.setText("White wins")
        elif status == STANDOFF:
            self.result_widget.label.setText("Stalemate")
        self.result_widget.show()

    def up_start(self):
        self.rounds.clear()
        self.rounds_2.clear()
        self.black_pieces.clear()
        self.white_pieces.clear()
        self.start_widget.show()

    @pyqtSlot()
    def start(self):
        self.start_widget.hide()
        self.board_widget.setDisabled(False)

        time = self.start_widget.get_game_time()
        side = self.start_widget.get_bot_side()

        self.board_widget.start_game(side)

        self.times[0] = time
        self.times[1] = time

        self.timer_pl1.setText(time.toString())
        self.timer_pl2.setText(time.toString())

        self.timers[1].start(1000)

    @pyqtSlot(bool)
    def timer_control(self, turn):
        if turn:
            self.timers[0].stop()
            self.timers[1].start(1000)
        else:
            self.timers[1].stop()
            self.timers[0].start(1000)

    def show_time(self, index):
        if self.times[index] == QTime(0, 0, 0):
            self.timers[index].stop()
            print(1)
            return
        self.times[index] = self.times[index].addSecs(-1)
        if index == 0:
            self.timer_pl1.setText(self.times[0].toString('hh:mm:ss'))
        else:
            self.timer_pl2.setText(self.times[1].toString('hh:mm:ss'))

    @pyqtSlot(bool)
    def update_taken_pieces(self, turn):
        if turn:
            self.black_pieces.show_taken_pieces(self.board_widget.get_taken_pieces(0))
        else:
            self.white_pieces.show_taken_pieces(self.board_widget.get_taken_pieces(1))

    @pyqtSlot(str)
    def update_steps(self, a0):
        if self.board_widget.game.rounds % 2 != 0:
            self.rounds.append(f"{self.board_widget.game.current_round}:{a0}")
        else:
            self.rounds_2.append(a0)


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    GameWindow.window = GameWindow()
    GameWindow.window.show()
    sys.exit(app.exec_())
