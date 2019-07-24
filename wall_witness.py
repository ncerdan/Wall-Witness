""" Imports """
# Public
import sys
from PyQt4 import uic, QtGui, QtCore
import matplotlib.pyplot as plt
import dateutil.relativedelta

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

    axOptionsList = ['--',
                     'Session - Average Grade',
                     'Session - High Grade',
                     'Workout - Bench Press',
                     'Workout - One-Arm Negative',
                     'Workout - Pistol Squat',
                     'Body Weight']

    marshalled_options = {
        'Session - Average Grade': 'avGr',
        'Session - High Grade': 'hiGr',
        'Workout - Bench Press': 'bench',
        'Workout - One-Arm Negative': 'neg',
        'Workout - Pistol Squat': 'pistol',
        'Body Weight': 'weight'
    }


    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Setup exit action and shortcut
        self.actionExit.triggered.connect(self.close_app)
        self.actionExit.setShortcut('ctrl+Q')

        # Setup axis options
        self.lAxBox.clear()
        self.rAxBox.clear()
        self.lAxBox.addItems(self.axOptionsList)
        self.rAxBox.addItems(self.axOptionsList)

        # Define default dates for calendars as system date-1 month, and system date
        today = QtCore.QDate.currentDate()
        lastMonth = today.addMonths(-1)
        self.startDateEdit.setDate(lastMonth)
        self.endDateEdit.setDate(today)

        # Setup button handlers
        self.setup_buttons()

        # Setup up empty graph
        self.canvas.figure.add_subplot(111).plot()

    def setup_buttons(self):
        # Set session, workout, and weight buttons
        self.sessionBtn.clicked.connect(self.launch_session)
        self.workoutBtn.clicked.connect(self.launch_workout)
        self.weightBtn.clicked.connect(self.launch_weight)

        # Set updates to graph when options or dates change
        self.lAxBox.currentIndexChanged.connect(self.left_axis_change)
        self.rAxBox.currentIndexChanged.connect(self.right_axis_change)
        self.startDateEdit.dateChanged.connect(self.start_date_change)
        self.endDateEdit.dateChanged.connect(self.end_date_change)

    # Redirection functions
    def launch_session(self): self.launch_dialog(SESSION)
    def launch_workout(self): self.launch_dialog(WORKOUT)
    def launch_weight(self):  self.launch_dialog(WEIGHT)

    # Handles launching session, workout, or weight dialogs based on type
    def launch_dialog(self, type):
        if (type == SESSION):   dialog = SessionUILogic.SessionUILogic(self)
        elif (type == WORKOUT): dialog = WorkoutUILogic.WorkoutUILogic(self)
        else:                   dialog = WeightUILogic.WeightUILogic(self)
        dialog.exec_()

    # Handle closing application
    def close_app(self): sys.exit()

    # Handle when user changes left axis option
    def left_axis_change(self):
        print("left change")

    # Handle when user changes right axis option
    def right_axis_change(self):
        print("right change")

    # Handle when user changes start date
    def start_date_change(self):
        print("start change")

    # Handle when user changes end date
    def end_date_change(self):
        print("end change")

    # Testing
    def plot(self):
        """
        ax = self.canvas.figure.add_subplot(111)
        ax.plot([1, 2, 3, 4])
        """

"""  Main Routine """
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainUILogic()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
