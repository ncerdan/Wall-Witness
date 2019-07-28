""" Imports """
# Public
import sys
from PyQt4 import uic, QtGui, QtCore
import matplotlib.pyplot as plt
from datetime import date, timedelta
import matplotlib.dates as mdates

import random

# Personal
import SessionUILogic, WorkoutUILogic, WeightUILogic, db_ops

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
                     'Boulder - Average Grade',
                     'Boulder - High Grade',
                     'Toprope - Average Grade',
                     'Toprope - High Grade',
                     'Sport   - Average Grade',
                     'Sport   - High Grade',
                     'Bench Press - High Weight',
                     'Bench Press - Average Weight',
                     'Bench Press - Sets',
                     'Bench Press - Reps',
                     'One-Arm Negative - High Weight',
                     'One-Arm Negative - Average Weight',
                     'One-Arm Negative - Sets',
                     'One-Arm Negative - Reps',
                     'Pistol Squat - High Weight',
                     'Pistol Squat - Average Weight',
                     'Pistol Squat - Sets',
                     'Pistol Squat - Reps',
                     'Body Weight']

    marshalled_options = {
        'Boulder - Average Grade':           'SBavGr',
        'Boulder - High Grade' :             'SBhiGr',
        'Toprope - Average Grade':           'STavGr',
        'Toprope - High Grade':              'SThiGr',
        'Sport   - Average Grade':           'SSavGr',
        'Sport   - High Grade':              'SShiGr',
        'Bench Press - High Weight':         'WBhiWt',
        'Bench Press - Average Weight':      'WBavWt',
        'Bench Press - Sets':                'WBsets',
        'Bench Press - Reps':                'WBreps',
        'One-Arm Negative - High Weight':    'WOhiWt',
        'One-Arm Negative - Average Weight': 'WOavWt',
        'One-Arm Negative - Sets':           'WOsets',
        'One-Arm Negative - Reps':           'WOreps',
        'Pistol Squat - High Weight':        'WPhiWt',
        'Pistol Squat - Average Weight':     'WPavWt',
        'Pistol Squat - Sets':               'WPsets',
        'Pistol Squat - Reps':               'WPreps',
        'Body Weight':                       'Bwght'
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

        # Set DateEdit restrictions
        self.reapply_date_restrictions()

        # Setup button handlers
        self.setup_buttons()

        # Setup subplots and set them to be empty (FIX!!! with transparent background?)
        self.lAx = self.canvas.figure.subplots()
        self.rAx = self.lAx.twinx()
        self.update_plot(CLEAR_BOTH)
        self.canvas.figure.patch.set_facecolor('#FFFFFF')

        # Setup list of dates for graph and x-axis format
        self.lAx.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU, interval=2))
        self.lAx.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        self.lAx.xaxis.set_minor_locator(mdates.DayLocator())
        self.update_date_range()

    def setup_buttons(self):
        # Set session, workout, and weight buttons
        self.sessionBtn.clicked.connect(self.launch_session)
        self.workoutBtn.clicked.connect(self.launch_workout)
        self.weightBtn.clicked.connect(self.launch_weight)

        # Set updates to graph when options or dates change
        self.lAxBox.currentIndexChanged.connect(self.left_axis_change)
        self.rAxBox.currentIndexChanged.connect(self.right_axis_change)
        self.startDateEdit.dateChanged.connect(self.update_date_range)
        self.endDateEdit.dateChanged.connect(self.update_date_range)

    # Redirection functions for launching dialogs
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

    # Handle a change to the y-axes
    def update_plot(self, type):
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
        elif type == UPDATE_LEFT or type == UPDATE_RIGHT:
            if type == UPDATE_LEFT:
                self.lAx.clear()
                type = self.marshalled_options[self.lAxBox.currentText()]
            else:
                self.rAx.clear()
                type = self.marshalled_options[self.rAxBox.currentText()]

            start = self.startDateEdit.dateTime().toPyDateTime()
            end   = self.endDateEdit.dateTime().toPyDateTime()
            x, y = db_ops.get_data_points(start, end, type)

            if type == UPDATE_LEFT:
                self.lAx.plot(x, y, 'b')
            else:
                self.rAx.plot(x, y, 'b')

        self.canvas.figure.canvas.draw()

    # Set x-axis to start and end values from dateEdit's
    def update_date_range(self):
        start = self.startDateEdit.dateTime().toPyDateTime()
        end   = self.endDateEdit.dateTime().toPyDateTime()
        delta = end - start
        self.dateRange = [start + timedelta(days=i) for i in range(delta.days + 1)]
        self.lAx.set_xlim(start, end)

        """
        * here: add check to delta and possibly customize major_locator based on its new value
        """

        self.canvas.figure.canvas.draw()
        self.reapply_date_restrictions()

    # Resets max and min dates on dateEdit's to ensure no conflicts
    def reapply_date_restrictions(self):
        self.startDateEdit.setMaximumDate(self.endDateEdit.date().toPyDate() + timedelta(days=-1))
        self.endDateEdit.setMinimumDate(self.startDateEdit.date().toPyDate() + timedelta(days=1))

"""  Main Routine """
def main():
    app = QtGui.QApplication(sys.argv)
    ui = MainUILogic()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
