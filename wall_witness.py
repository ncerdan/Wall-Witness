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

# main routine
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainUILogic()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
