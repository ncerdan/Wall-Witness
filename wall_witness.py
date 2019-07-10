""" Imports """
# Public
import sys
from PyQt4 import uic, QtGui, QtCore

# Personal
import SessionUILogic, WorkoutUILogic, WeightUILogic

""" Definitions """
SESSION = 0
WORKOUT = 1
WEIGHT  = 2

""" UI Class """
# load ui file for main layout
MainWindowUI, MainWindowBase = uic.loadUiType("ui/mainWindow.ui")

# use loaded ui file in ui logic class
class MainUILogic(MainWindowBase, MainWindowUI):
    def __init__(self, parent=None):
        super(MainUILogic, self).__init__(parent)
        self.setupUi(self)

        # Setup exit action and shortcut
        self.actionExit.triggered.connect(self.close_app)
        self.actionExit.setShortcut('ctrl+Q')

        # Setup button handlers
        self.setup_buttons()

    def setup_buttons(self):
        # Set session, workout, and weight buttons
        self.sessionBtn.clicked.connect(self.launch_session)
        self.workoutBtn.clicked.connect(self.launch_workout)
        self.weightBtn.clicked.connect(self.launch_weight)

        self.sessionBtn.move(10, 10)

    # Redirection functions
    def launch_session(self): self.launch_dialog(SESSION)
    def launch_workout(self): self.launch_dialog(WORKOUT)
    def launch_weight(self):  self.launch_dialog(WEIGHT)

    # Handles launching session, workout, or weight dialogs based on type
    def launch_dialog(self, type):
        dialog = QtGui.QDialog()
        if (type == SESSION):   dialog.ui = SessionUILogic.SessionUILogic()
        elif (type == WORKOUT): dialog.ui = WorkoutUILogic.WorkoutUILogic()
        else:                   dialog.ui = WeightUILogic.WeightUILogic()

        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    # Handle closing application
    def close_app(self): sys.exit()

"""  Main Routine """
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainUILogic()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
