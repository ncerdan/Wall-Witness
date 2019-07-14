""" Import  """
# Public
from PyQt4 import QtGui, uic, QtCore

# Personal
import db_ops

""" UI Class """
# load ui file for main layout
SessionDialogUI, SessionDialogBase = uic.loadUiType("ui/sessionDialog.ui")

# use loaded ui file in ui logic class
class SessionUILogic(SessionDialogBase, SessionDialogUI):

    typesList = ['--', 'Boulder', 'Top-Rope', 'Sport']
    marshalled_type = {
        'Boulder': 'boulder',
        'Top-Rope': 'toprope',
        'Sport': 'sport'
    }

    envrList  = ['--', 'Indoors', 'Outdoors']
    marshalled_envr = {
        'Indoors': 'in',
        'Outdoors': 'out'
    }

    unitsList = ['hr', 'min']

    bldrList  = ['--', 'V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12']
    ropeList  = ['--', '5.9',
                       '5.10a', '5.10b', '5.10c', '5.10d',
                       '5.11a', '5.11b', '5.11c', '5.11d',
                       '5.12a', '5.12b', '5.12c', '5.12d',
                       '5.13a', '5.13b', '5.13c', '5.13d']
    marshalled_grades = {
        # Bouldering grade mappings
        'V0': 0, 'V1': 1, 'V2': 2,  'V3': 3,   'V4': 4,   'V5': 5,   'V6': 6,
        'V7': 7, 'V8': 8, 'V9': 9, 'V10': 10, 'V11': 11, 'V12': 12, 'V13': 13,

        # Rope grade mappings
          '5.9': 9.00,
        '5.10a': 10.00, '5.10b': 10.25, '5.10c': 10.50, '5.10d': 10.75,
        '5.11a': 11.00, '5.11b': 11.25, '5.11c': 11.50, '5.11d': 11.75,
        '5.12a': 12.00, '5.12b': 12.25, '5.12c': 12.50, '5.12d': 12.75,
        '5.13a': 13.00, '5.13b': 13.25, '5.13c': 13.50, '5.13d': 13.75
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)

        # Add type options
        self.typeBox.clear()
        self.typeBox.addItems(self.typesList)

        # Add environment options
        self.envrBox.clear()
        self.envrBox.addItems(self.envrList)

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

        # Set up custom warning text
        self.warningLabel.setStyleSheet('QLabel#warningLabel {color: red}')
        self.warningLabel.hide()

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
            to_add = self.bldrList
        else:
            to_add = self.ropeList

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
        date = self.dateEdit.date().toPyDate()
        locn = self.locnEdit.text()
        durn = float(self.durnEdit.text())
        dnUt = str(self.durnUnitsBox.currentText())
        avGr = str(self.avGrBox.currentText())
        hiGr = str(self.hiGrBox.currentText())
        note = self.noteEdit.toPlainText()

        # Marshall data that will be represeneted in DB differently
        type = self.marshalled_type[type]
        envr = self.marshalled_envr[envr]
        avGr = float(self.marshalled_grades[avGr])
        hiGr = float(self.marshalled_grades[hiGr])

        # Possibly convert duration from min -> hr
        if dnUt == 'min': durn = durn / 60

        # Round duration entry
        durn = round(durn, 2)

        """   TESTING
        print("type: " + type)
        print("envr: " + envr)
        print("date: " + str(date))
        print("locn: " + locn)
        print("durn: " + str(durn))
        print("dnUt: " + dnUt)
        print("avGr: " + str(avGr))
        print("hiGr: " + str(hiGr))
        print("note: " + note)
         END TESTING """

        # Add new entry into the database
        """   TESTING   """
        if self.toggleDB.isChecked():
            print('sent to DB')
            """ END TESTING """
            db_ops.add_session(type, envr, avGr, hiGr, date, durn, locn, note)

        # Close dialog
        self.close_dialog()

    def close_dialog(self): self.done(1)


