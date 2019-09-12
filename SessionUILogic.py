""" Imports """
# Public
from PyQt4 import QtGui, uic, QtCore

# Personal
import constants

""" UI Class """
# Load ui file for dialog layout
SessionDialogUI, SessionDialogBase = uic.loadUiType("ui/sessionDialog.ui")

# Use loaded ui file in ui logic class
class SessionUILogic(SessionDialogBase, SessionDialogUI):
    def __init__(self, parent=None, dbops=None):
        if dbops == None:
            return

        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        # Save database operations object
        self.db_ops = dbops

        # Add type options
        self.typeBox.clear()
        self.typeBox.addItems(constants.session_types_ist)

        # Add environment options
        self.envrBox.clear()
        self.envrBox.addItems(constants.session_envr_list)

        # Define default date for calendar as system date
        self.dateEdit.setDate(QtCore.QDate.currentDate())

        # Placeholder for location
        self.locnEdit.setPlaceholderText('drg')

        # Ensure duration input is float
        floatValidator = QtGui.QDoubleValidator()
        self.durnEdit.setValidator(floatValidator)
        self.durnEdit.setPlaceholderText('0')

        # Add duration unit options
        self.durnUnitsBox.clear()
        self.durnUnitsBox.addItems(constants.time_units_list)

        # Add avGr options
        self.avGrBox.clear()
        self.avGrBox.addItem('--')

        # Add hiGr options
        self.hiGrBox.clear()
        self.hiGrBox.addItem('--')

        # Setup custom warning text
        self.warningLabel.setStyleSheet('QLabel#warningLabel {color: red}')
        self.warningLabel.hide()

        self.setup_buttons()

    def setup_buttons(self):
        self.submitBtn.clicked.connect(self.submit_entry)
        self.cancelBtn.clicked.connect(self.close_dialog)
        self.typeBox.currentIndexChanged.connect(self.type_change)

    def type_change(self):
        new_type = self.typeBox.currentText()
        if new_type == '--':
            self.avGrBox.clear()
            self.hiGrBox.clear()
            self.avGrBox.addItem('--')
            self.hiGrBox.addItem('--')
            return
        elif new_type == 'Boulder':
            to_add = constants.bldr_grade_list
        else:
            to_add = constants.rope_grade_list

        self.avGrBox.clear()
        self.hiGrBox.clear()
        self.avGrBox.addItems(to_add)
        self.hiGrBox.addItems(to_add)

    def create_and_show_warning(self, missing):
        self.warningLabel.setText("Oops! You need to input " + missing + ".")
        self.warningLabel.show()

    def submit_entry(self):
        # Check that the user entered all data
        if self.typeBox.currentText() == "--":
            self.create_and_show_warning('a type')
            return
        if self.envrBox.currentText() == "--":
            self.create_and_show_warning('an environment')
            return
        if self.locnEdit.text() == "":
            self.create_and_show_warning('a location')
            return
        if self.durnEdit.text() == "":
            self.create_and_show_warning('a duration')
            return
        if self.avGrBox.currentText() == "--":
            self.create_and_show_warning('an average grade')
            return
        if self.hiGrBox.currentText() == "--":
            self.create_and_show_warning('a max grade')
            return

        # Get data from inputs
        type = str(self.typeBox.currentText())
        envr = str(self.envrBox.currentText())
        date = self.dateEdit.dateTime().toPyDateTime()
        locn = self.locnEdit.text()
        durn = float(self.durnEdit.text())
        dnUt = str(self.durnUnitsBox.currentText())
        avGr = str(self.avGrBox.currentText())
        hiGr = str(self.hiGrBox.currentText())
        note = self.noteEdit.toPlainText()

        # Marshall data that will be represeneted in DB differently
        type = constants.marshalled_session_types[type]
        envr = constants.marshalled_session_envr[envr]
        avGr = float(constants.marshalled_grades[avGr])
        hiGr = float(constants.marshalled_grades[hiGr])

        # Possibly convert duration from min -> hr
        if dnUt == 'min': durn = durn / 60

        # Round duration entry
        durn = round(durn, 2)

        # Add new entry into the database
        self.db_ops.add_session(type, envr, avGr, hiGr, date, durn, locn, note)

        # Close dialog
        self.close_dialog()

    def close_dialog(self): self.done(1)
