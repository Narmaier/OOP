from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTime
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QButtonGroup
from Square import BLACK, WHITE
from UIs.startUI import Ui_Form as StartUI
from UIs.settingsUI import Ui_Form as SettingsUI
from UIs.resultUI import Ui_Form as ResultUI
from PyQt5 import QtCore

class StartMenu(QWidget, StartUI):
    close = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = None
        self.setupUi(self)
        self.pushButton_2.pressed.connect(self.up_settings)

        self.widget = Settings(self)
        self.widget.hide()

    def up_settings(self):
        self.widget.setFocus()
        self.widget.show()

    def get_game_time(self):
        return self.widget.timeEdit.time()

    def get_bot_side(self):
        return self.widget.BotSide


class Settings(QWidget, SettingsUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.timeEdit.setTime(QTime(0, 30, 0))
        self.radioButton.toggled.connect(lambda: self.change_state(BLACK))
        self.radioButton_2.toggled.connect(lambda: self.change_state(WHITE))
        self.radioButton_3.toggled.connect(lambda: self.change_state(None))
        self.BotSide = None

        self.radioButton_3.setChecked(True)

    def change_state(self, game_state):
        self.BotSide = game_state

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()


class Result(QWidget, ResultUI):
    def __init__(self, result: str, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.label.setText(result)
        self.pushButton.pressed.connect(self.close)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = StartMenu()
    widget.show()
    sys.exit(app.exec_())
