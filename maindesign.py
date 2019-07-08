# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maindesign.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WallWitness(object):
    def setupUi(self, WallWitness):
        WallWitness.setObjectName(_fromUtf8("WallWitness"))
        WallWitness.resize(875, 609)
        self.centralwidget = QtGui.QWidget(WallWitness)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.submitBtn = QtGui.QPushButton(self.centralwidget)
        self.submitBtn.setGeometry(QtCore.QRect(190, 180, 93, 28))
        self.submitBtn.setObjectName(_fromUtf8("submitBtn"))
        self.typeBox = QtGui.QComboBox(self.centralwidget)
        self.typeBox.setGeometry(QtCore.QRect(70, 60, 121, 22))
        self.typeBox.setObjectName(_fromUtf8("typeBox"))
        self.envBox = QtGui.QComboBox(self.centralwidget)
        self.envBox.setGeometry(QtCore.QRect(210, 60, 121, 22))
        self.envBox.setObjectName(_fromUtf8("envBox"))
        self.AvGrTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.AvGrTextEdit.setGeometry(QtCore.QRect(370, 60, 104, 31))
        self.AvGrTextEdit.setObjectName(_fromUtf8("AvGrTextEdit"))
        self.HiGrTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.HiGrTextEdit.setGeometry(QtCore.QRect(490, 60, 104, 31))
        self.HiGrTextEdit.setObjectName(_fromUtf8("HiGrTextEdit"))
        self.dateEdit = QtGui.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(620, 60, 110, 22))
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.durnTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.durnTextEdit.setGeometry(QtCore.QRect(120, 120, 104, 31))
        self.durnTextEdit.setObjectName(_fromUtf8("durnTextEdit"))
        self.locnTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.locnTextEdit.setGeometry(QtCore.QRect(250, 120, 104, 31))
        self.locnTextEdit.setObjectName(_fromUtf8("locnTextEdit"))
        self.noteTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.noteTextEdit.setGeometry(QtCore.QRect(390, 120, 361, 91))
        self.noteTextEdit.setObjectName(_fromUtf8("noteTextEdit"))
        WallWitness.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(WallWitness)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 875, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        WallWitness.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(WallWitness)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        WallWitness.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(WallWitness)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(WallWitness)
        QtCore.QMetaObject.connectSlotsByName(WallWitness)

    def retranslateUi(self, WallWitness):
        WallWitness.setWindowTitle(_translate("WallWitness", "Wall Witness", None))
        self.submitBtn.setText(_translate("WallWitness", "PushButton", None))
        self.menuFile.setTitle(_translate("WallWitness", "File", None))
        self.actionExit.setText(_translate("WallWitness", "Exit", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    WallWitness = QtGui.QMainWindow()
    ui = Ui_WallWitness()
    ui.setupUi(WallWitness)
    WallWitness.show()
    sys.exit(app.exec_())

