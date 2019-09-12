""" Imports """
# Public
from PyQt4 import QtGui, uic, QtCore

# Personal
import constants

""" UI Class """
# Load ui file for dialog layout
WeightDialogUI, WeightDialogBase = uic.loadUiType("ui/weightDialog.ui")

# Use loaded ui file in ui logic class
class WeightUILogic(WeightDialogBase, WeightDialogUI):
    def __init__(self, parent=None, dbops=None):
        if dbops == None:
            return

        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        # Save database operations object
        self.db_ops = dbops

        # Ensure weight input is double
        doubleValidator = QtGui.QDoubleValidator()
        self.weightEdit.setValidator(doubleValidator)
        self.weightEdit.setPlaceholderText("0.0")

        # Add units options
        self.unitsBox.clear()
        self.unitsBox.addItems(constants.weight_units_list)

        # Define default date for calendar as system date
        self.dateEdit.setDate(QtCore.QDate.currentDate())

        # Setup custom warning text
        self.warningLabel.setStyleSheet('QLabel#warningLabel {color: red}')
        self.warningLabel.hide()

        # Setup button connections
        self.setup_buttons()

    def setup_buttons(self):
        self.submitBtn.clicked.connect(self.submit_entry)
        self.cancelBtn.clicked.connect(self.close_dialog)

    def submit_entry(self):
        # Check that the user entered a weight
        if self.weightEdit.text() == "":
            self.warningLabel.show()
            return

        # Get data from inputs
        weight = float(self.weightEdit.text())
        units =  str(self.unitsBox.currentText())
        date =   self.dateEdit.dateTime().toPyDateTime()

        # Possibly convert weight from kg to lbs
        if units == 'kg':
            weight = weight * 2.205

        # Round weight entry
        weight = round(weight, 1)

        # Add new entry into the database
        self.db_ops.add_weight(date, weight)

        # Close dialog
        self.close_dialog()

    def close_dialog(self): self.done(1)
