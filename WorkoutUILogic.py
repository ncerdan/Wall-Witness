""" Import  """
# Public
from PyQt4 import QtGui, uic, QtCore

# Personal
import db_ops

""" UI Class """
# load ui file for main layout
WorkoutDialogUI, WorkoutDialogBase = uic.loadUiType("ui/workoutDialog.ui")

# use loaded ui file in ui logic class
class WorkoutUILogic(WorkoutDialogBase, WorkoutDialogUI):

    typesList = ['--', 'Bench Press', '1-Arm Negative', 'Pistol Squat']
    unitsList = ['lbs', 'kg']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        # Add type options
        self.typeBox.clear()
        self.typeBox.addItems(self.typesList)

        # Define default date for calendar as system date
        self.dateEdit.setDate(QtCore.QDate.currentDate())

        # Ensure sets input is int
        intValidator = QtGui.QIntValidator()
        self.setsEdit.setValidator(intValidator)
        self.setsEdit.setPlaceholderText("0")

        # Ensure reps input is float
        doubleValidator1 = QtGui.QDoubleValidator()
        self.repsEdit.setValidator(doubleValidator1)
        self.repsEdit.setPlaceholderText("0.0")

        # Ensure avWt input is float
        doubleValidator2 = QtGui.QDoubleValidator()
        self.avWtEdit.setValidator(doubleValidator2)
        self.avWtEdit.setPlaceholderText("0.0")

        # Add average weight units options
        self.avWtUnitsBox.clear()
        self.avWtUnitsBox.addItems(self.unitsList)

        # Ensure hiWt input is float
        doubleValidator3 = QtGui.QDoubleValidator()
        self.hiWtEdit.setValidator(doubleValidator3)
        self.hiWtEdit.setPlaceholderText("0.0")

        # Add average weight units options
        self.hiWtUnitsBox.clear()
        self.hiWtUnitsBox.addItems(self.unitsList)

        # Set up custom warning text
        self.warningLabel.setStyleSheet('QLabel#warningLabel {color: red}')
        self.warningLabel.hide()

        # Setup button connections
        self.setup_buttons()

        """   TESTING   """
        self.toggleDB = QtGui.QCheckBox(self)
        self.toggleDB.move(50, 250)
        self.toggleDB.setChecked(False)
        self.toggleDB.show()
        """ END TESTING """

    def setup_buttons(self):
        self.submitBtn.clicked.connect(self.submit_entry)
        self.cancelBtn.clicked.connect(self.close_dialog)

    def create_and_show_warning(self, missing):
        self.warningLabel.setText("Oops! You need to input " + missing + ".")
        self.warningLabel.show()

    def submit_entry(self):
        # Check that the user entered all data
        if self.typeBox.currentText() == "--":
            self.create_and_show_warning('a type')
            return
        if self.setsEdit.text() == "":
            self.create_and_show_warning('a set count')
            return
        if self.repsEdit.text() == "":
            self.create_and_show_warning('a rep count')
            return
        if self.avWtEdit.text() == "":
            self.create_and_show_warning('an average weight')
            return
        if self.hiWtEdit.text() == "":
            self.create_and_show_warning('a max weight')
            return

        # Get data from inputs
        type = str(self.typeBox.currentText())
        date = self.dateEdit.date().toPyDate()
        sets = self.setsEdit.text()
        reps = self.repsEdit.text()
        avWt = float(self.avWtEdit.text())
        avUt = str(self.avWtUnitsBox.currentText())
        hiWt = float(self.hiWtEdit.text())
        hiUt = str(self.hiWtUnitsBox.currentText())

        # Convert type format to how it will stored in DB
        if type == 'Bench Press':
            type = 'bench'
        elif type == '1-Arm Negative':
            type = 'neg'
        elif type == 'Pistol Squat':
            type = 'pistol'

        # Possibly convert weight from kg -> lbs
        if avUt == 'kg':
            avWt = avWt * 2.205

        if hiUt == 'kg':
            hiWt = hiWt * 2.205

        # Round weight entries
        avWt = round(avWt, 1)
        hiWt = round(hiWt, 1)

        # Add new entry into the database
        """   TESTING   """
        if self.toggleDB.isChecked():
            print('sent to DB')
            """ END TESTING """
            db_ops.add_workout(type, date, sets, reps, avWt, hiWt)

        # Close dialog
        self.close_dialog()

    def close_dialog(self): self.done(1)





