""" Imports """
# Public
import sys
from PyQt4 import uic, QtGui

""" UI Class """
# load ui file for main layout
baseUIClass, baseUIWidget = uic.loadUiType("maindesign.ui")

# use loaded ui file in ui logic class
class MainUILogic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(MainUILogic, self).__init__(parent)
        self.setupUi(self)

        # Set exit button and shortcut
        self.actionExit.triggered.connect(self.close_app)
        self.actionExit.setShortcut('ctrl+Q')

    def close_app(self):
        sys.exit()

# main routine
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainUILogic()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
