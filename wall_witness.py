""" Imports """
# Public
import sys
from PyQt4 import uic, QtGui, QtCore
import matplotlib.pyplot as plt
from datetime import date, timedelta
import matplotlib.dates as mdates

# Personal
from SessionUILogic import SessionUILogic
from WorkoutUILogic import WorkoutUILogic
from WeightUILogic import WeightUILogic
from db_ops import DBOps
import constants

""" UI Class """
# Load ui file for main layout
MainWindowUI, MainWindowBase = uic.loadUiType("ui/mainWindow.ui")

# Use loaded ui file in ui logic class
class MainUILogic(MainWindowBase, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Initialize database operations object
        self.db_ops = DBOps()

        # Setup exit action and shortcut
        self.actionExit.triggered.connect(self.close_app)
        self.actionExit.setShortcut('ctrl+Q')

        # Setup axis options
        self.lAxBox.clear()
        self.rAxBox.clear()
        self.lAxBox.addItems(constants.graph_ax_options_list)
        self.rAxBox.addItems(constants.graph_ax_options_list)

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
        self.update_plot(constants.CLEAR_BOTH)
        self.canvas.figure.patch.set_facecolor('#FFFFFF')

        # Setup x-axis format
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

        # Set calendar reset button handler
        self.resetBtn.clicked.connect(self.reset_dates)

        # Set graph refresh button handler
        self.refreshBtn.clicked.connect(self.update_date_range)

    # Redirection functions for launching dialogs
    def launch_session(self): self.launch_dialog(constants.SESSION)
    def launch_workout(self): self.launch_dialog(constants.WORKOUT)
    def launch_weight(self):  self.launch_dialog(constants.WEIGHT)

    # Handles launching session, workout, or weight dialogs based on type
    def launch_dialog(self, type):
        if   (type == constants.SESSION): dialog = SessionUILogic(self, dbops=self.db_ops)
        elif (type == constants.WORKOUT): dialog = WorkoutUILogic(self, dbops=self.db_ops)
        else:                             dialog = WeightUILogic(self, dbops=self.db_ops)
        dialog.exec_()

    # Handle closing application
    def close_app(self): sys.exit()

    # Handle when user changes left axis option
    def left_axis_change(self):
        new = self.lAxBox.currentText()
        if new == "--": self.update_plot(constants.CLEAR_LEFT)
        else:           self.update_plot(constants.UPDATE_LEFT)

    # Handle when user changes right axis option
    def right_axis_change(self):
        new = self.rAxBox.currentText()
        if new == "--": self.update_plot(constants.CLEAR_RIGHT)
        else:           self.update_plot(constants.UPDATE_RIGHT)

    # Handle a change to the y-axes
    def update_plot(self, type):
        if type == constants.CLEAR_BOTH:
            self.lAx.clear()
            self.rAx.clear()
            self.lAx.plot()
            self.rAx.plot()
        elif type == constants.CLEAR_LEFT:
            self.lAx.clear()
            self.lAx.plot()
        elif type == constants.CLEAR_RIGHT:
            self.rAx.clear()
            self.rAx.plot()
        elif type == constants.UPDATE_LEFT:
            start = self.startDateEdit.dateTime().toPyDateTime()
            end   = self.endDateEdit.dateTime().toPyDateTime()
            type  = constants.marshalled_graph_ax_options[self.lAxBox.currentText()]
            x, y  = self.db_ops.get_data_points(start, end, type)
            self.lAx.clear()
            if x != None and y != None:
                self.lAx.plot(x, y, 'b')
        elif type == constants.UPDATE_RIGHT:
            start = self.startDateEdit.dateTime().toPyDateTime()
            end   = self.endDateEdit.dateTime().toPyDateTime()
            type  = constants.marshalled_graph_ax_options[self.rAxBox.currentText()]
            x, y  = self.db_ops.get_data_points(start, end, type)
            self.rAx.clear()
            if x != None and y != None:
                self.rAx.plot(x, y, 'r')

        self.set_date_range()
        self.canvas.figure.canvas.draw()

    # Set x-axis granularity to avoid overlap
    def set_xaxis_granularity(self, granularity):
        xaxis = self.lAx.xaxis

        if granularity == constants.DAILY:
            xaxis.set_major_locator(mdates.DayLocator())
            xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        elif granularity == constants.WEEKLY:
            xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU))
            xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            xaxis.set_minor_locator(mdates.DayLocator())
        elif granularity == constants.BIWEEKLY:
            xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SU, interval=2))
            xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.SU))
        elif granularity == constants.MONTHLY:
            xaxis.set_major_locator(mdates.MonthLocator())
            xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))
            xaxis.set_minor_locator(mdates.DayLocator(bymonthday=15))
        elif granularity == constants.BIMONTHLY:
            xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))
            xaxis.set_minor_locator(mdates.DayLocator(bymonthday=1))
        elif granularity == constants.SIXMONTHLY:
            xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))
            xaxis.set_minor_locator(mdates.MonthLocator())
        elif granularity == constants.YEARLY:
            xaxis.set_major_locator(mdates.YearLocator())
            xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
            xaxis.set_minor_locator(mdates.MonthLocator(interval=3))

    # Set x-axis to start and end values from dateEdit's
    def set_date_range(self):
        start = self.startDateEdit.dateTime().toPyDateTime()
        end   = self.endDateEdit.dateTime().toPyDateTime()
        self.lAx.set_xlim(start, end)

        # Check new date delta and set new x-axis granularity
        delta = end - start
        days_delta = delta.days

        if   days_delta > 1200: self.set_xaxis_granularity(constants.YEARLY)
        elif days_delta > 525:  self.set_xaxis_granularity(constants.SIXMONTHLY)
        elif days_delta > 220:  self.set_xaxis_granularity(constants.BIMONTHLY)
        elif days_delta > 99:   self.set_xaxis_granularity(constants.MONTHLY)
        elif days_delta > 54:   self.set_xaxis_granularity(constants.BIWEEKLY)
        elif days_delta > 9:    self.set_xaxis_granularity(constants.WEEKLY)
        else:                   self.set_xaxis_granularity(constants.DAILY)

    # Update x-axis to start and end values from dateEdit's
    def update_date_range(self):
        self.set_date_range()

        self.left_axis_change()
        self.right_axis_change()

        self.canvas.figure.canvas.draw()
        self.reapply_date_restrictions()

    # Set dates back to original default values
    def reset_dates(self):
        today = QtCore.QDate.currentDate()
        lastMonth = today.addMonths(-1)
        self.startDateEdit.setDate(lastMonth)
        self.endDateEdit.setDate(today)

        self.update_date_range()

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
