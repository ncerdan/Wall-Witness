""" Import  """
from PyQt4 import QtGui, uic, QtCore

""" UI Class """
# load ui file for main layout
WeightDialogUI, WeightDialogBase = uic.loadUiType("ui/weightDialog.ui")

# use loaded ui file in ui logic class
class WeightUILogic(WeightDialogBase, WeightDialogUI):
    def __init__(self, parent=None):
        super(WeightUILogic, self).__init__(parent)
        self.setupUi(self)

        self.setup_buttons()

    def setup_buttons(self):
        self.submitBtn.clicked.connect(self.submit_entry)
        self.cancelBtn.clicked.connect(self.close_dialog)

    def submit_entry(self):
        print("Submit!")
        print("Weight: " + self.weightEdit.text())
        self.close_dialog()

    def close_dialog(self):
        print("Closing!")
