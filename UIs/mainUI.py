# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Downloads\main(1).ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(729, 741)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lletters = QtWidgets.QLabel(self.centralwidget)
        self.lletters.setGeometry(QtCore.QRect(40, 621, 576, 24))
        self.lletters.setText("")
        self.lletters.setPixmap(QtGui.QPixmap("D:/OOP/svg/letters.jpg"))
        self.lletters.setObjectName("lletters")
        self.numbers = QtWidgets.QLabel(self.centralwidget)
        self.numbers.setGeometry(QtCore.QRect(11, 41, 24, 576))
        self.numbers.setText("")
        self.numbers.setPixmap(QtGui.QPixmap("D:/OOP/svg/numbers.jpg"))
        self.numbers.setObjectName("numbers")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 41, 576, 576))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.taken_white = QtWidgets.QGroupBox(self.centralwidget)
        self.taken_white.setGeometry(QtCore.QRect(15, 0, 601, 42))
        self.taken_white.setStyleSheet("QGroupBoxl{\n"
"\n"
"background-color: white;    \n"
"\n"
"}")
        self.taken_white.setTitle("")
        self.taken_white.setObjectName("taken_white")
        self.taken_black = QtWidgets.QGroupBox(self.centralwidget)
        self.taken_black.setGeometry(QtCore.QRect(15, 647, 601, 42))
        self.taken_black.setTitle("")
        self.taken_black.setObjectName("taken_black")
        self.rounds = QtWidgets.QTextBrowser(self.centralwidget)
        self.rounds.setGeometry(QtCore.QRect(624, 64, 50, 561))
        self.rounds.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rounds.setObjectName("rounds")
        self.timer_pl1 = QtWidgets.QLabel(self.centralwidget)
        self.timer_pl1.setGeometry(QtCore.QRect(623, 2, 101, 54))
        self.timer_pl1.setStyleSheet("QLabel{\n"
"\n"
"background-color: white;    \n"
"font-size:19pt\n"
"}")
        self.timer_pl1.setObjectName("timer_pl1")
        self.timer_pl2 = QtWidgets.QLabel(self.centralwidget)
        self.timer_pl2.setGeometry(QtCore.QRect(623, 631, 101, 54))
        self.timer_pl2.setStyleSheet("QLabel{\n"
"\n"
"background-color: white;    \n"
"font-size:19pt\n"
"}")
        self.timer_pl2.setObjectName("timer_pl2")
        self.rounds_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.rounds_2.setGeometry(QtCore.QRect(673, 64, 50, 561))
        self.rounds_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rounds_2.setObjectName("rounds_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 729, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.timer_pl1.setText(_translate("MainWindow", "99:99:99"))
        self.timer_pl2.setText(_translate("MainWindow", "99:99:99"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())