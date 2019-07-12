""" Import  """
# Public
from PyQt4 import QtGui, uic, QtCore

# Personal
import db_ops

""" UI Class """
# load ui file for main layout
WeightDialogUI, WeightDialogBase = uic.loadUiType("ui/weightDialog.ui")

# use loaded ui file in ui logic class
class WeightUILogic(WeightDialogBase, WeightDialogUI):

    weightUnitsList = ['lbs', 'kg']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        # Ensure weight input is double
        doubleValidator = QtGui.QDoubleValidator()
        self.weightEdit.setValidator(doubleValidator)
        self.weightEdit.setPlaceholderText("0.0")

        # Add units options
        self.unitsBox.clear()
        self.unitsBox.addItems(self.weightUnitsList)

        # Define default date for calendar as system date
        self.dateEdit.setDate(QtCore.QDate.currentDate())

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

    def submit_entry(self):
        # Check that the user entered a weight
        if self.weightEdit.text() == "":
            self.warningLabel.show()
            return

        # Get data from inputs
        weight = float(self.weightEdit.text())
        units =  str(self.unitsBox.currentText())
        date =   self.dateEdit.date().toPyDate()

        # Possibly convert weight from kg -> lbs
        if units == 'kg':
            weight = weight * 2.205

        # Round weight entry
        weight = round(weight, 1)

        # Add new entry into the database
        """   TESTING   """
        if self.toggleDB.isChecked():
            print('sent to DB')
            """ END TESTING """
            db_ops.add_weight(date, weight)

        # Close dialog
        self.close_dialog()

    def close_dialog(self): self.done(1)
