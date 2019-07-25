""" Imports """
# Public
import sys
from PyQt4 import uic, QtGui, QtCore
import matplotlib.pyplot as plt
from datetime import date, timedelta

import random

# Personal
import SessionUILogic, WorkoutUILogic, WeightUILogic

""" Definitions """
# Dialog control
SESSION = 0
WORKOUT = 1
WEIGHT  = 2

# Plotting control
CLEAR_BOTH   = 0
CLEAR_LEFT   = 1
CLEAR_RIGHT  = 2
UPDATE_LEFT  = 3
UPDATE_RIGHT = 4

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

        # Setup subplots and set them to be empty
        self.lAx = self.canvas.figure.subplots()
        self.rAx = self.lAx.twinx()
        self.update_plot(CLEAR_BOTH)

        # Setup list of dates for graph
        start = self.startDateEdit.date().toPyDate()
        end   = self.endDateEdit.date().toPyDate()
        delta = end - start
        self.dateRange = [start + timedelta(days=i) for i in range(delta.days + 1)]
        self.lAx.set_xlim(start, end)
        self.rAx.set_xlim(start, end)

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
        new = self.lAxBox.currentText()
        if new == "--":
            self.update_plot(CLEAR_LEFT)
        else:
            self.update_plot(UPDATE_LEFT)

    # Handle when user changes right axis option
    def right_axis_change(self):
        new = self.rAxBox.currentText()
        if new == "--":
            self.update_plot(CLEAR_RIGHT)
        else:
            self.update_plot(UPDATE_RIGHT)

    # Handle when user changes start date
    def start_date_change(self):
        print("start change")

    # Handle when user changes end date
    def end_date_change(self):
        print("end change")

    # Testing
    def update_plot(self, type):
        # Clear plotting if desired
        if type == CLEAR_BOTH:
            self.lAx.clear()
            self.rAx.clear()
            self.lAx.plot()
            self.rAx.plot()
        elif type == CLEAR_LEFT:
            self.lAx.clear()
            self.lAx.plot()
        elif type == CLEAR_RIGHT:
            self.rAx.clear()
            self.rAx.plot()
        elif type == UPDATE_LEFT:
            self.lAx.clear()
            new = [random.randint(0,10) for i in range(10)]
            self.lAx.plot(new, 'b')
        elif type == UPDATE_RIGHT:
            self.rAx.clear()
            new = [random.randint(0,10) for i in range(10)]
            self.rAx.plot(new, 'r')

        self.canvas.figure.canvas.draw()
        self.canvas.figure.canvas.draw()


"""  Main Routine """
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainUILogic()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
