""" Import  """
from PyQt4 import QtGui, uic, QtCore

""" UI Class """
# load ui file for main layout
SessionDialogUI, SessionDialogBase = uic.loadUiType("ui/sessionDialog.ui")

# use loaded ui file in ui logic class
class SessionUILogic(SessionDialogBase, SessionDialogUI):

    typesList = ['--', 'Bouldering', 'Top-Rope', 'Sport']
    envList   = ['--', 'in', 'out']
    unitsList = ['hr', 'min']
    bldrList  = ['--', 'V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13']
    ropeList  = ['--', '5.9',
                       '5.10a', '5.10b', '5.10c', '5.10d',
                       '5.11a', '5.11b', '5.11c', '5.11d',
                       '5.12a', '5.12b', '5.12c', '5.12d',
                       '5.13a', '5.13b', '5.13c', '5.13d']

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        # Add type options
        self.typeBox.clear()
        self.typeBox.addItems(self.typesList)

        # Add environment options
        self.envBox.clear()
        self.envBox.addItems(self.envList)

        # Define default date for calendar as system date
        self.dateEdit.setDate(QtCore.QDate.currentDate())

        # Placeholder for location
        self.locnEdit.setPlaceholderText('drg')

        # Ensure duration input is float
        floatValidator = QtGui.QDoubleValidator()
        self.durnEdit.setValidator(floatValidator)
        self.durnEdit.setPlaceholderText('0')

        # Add unit options
        self.durnUnitsBox.clear()
        self.durnUnitsBox.addItems(self.unitsList)

        # Add avGr options
        self.avGrBox.clear()
        self.avGrBox.addItem('--')

        # Add hiGr options
        self.hiGrBox.clear()
        self.hiGrBox.addItem('--')

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
        # Check that the user entered all data

        # Get data from inputs

        # Add new entry into the database
        """   TESTING   """
        if self.toggleDB.isChecked():
            print('sent to DB')
            """ END TESTING """
            #db_ops.add_session()

        # Close dialog
        self.close_dialog()

    def close_dialog(self): self.done(1)


