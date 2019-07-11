""" Import  """
from PyQt4 import QtGui, uic, QtCore

""" UI Class """
# load ui file for main layout
WeightDialogUI, WeightDialogBase = uic.loadUiType("ui/weightDialog.ui")

# use loaded ui file in ui logic class
class WeightUILogic(WeightDialogBase, WeightDialogUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        
        self.setup_buttons()

    def setup_buttons(self):
        self.submitBtn.clicked.connect(self.submit_entry)
        self.cancelBtn.clicked.connect(self.close_dialog)

    def submit_entry(self):
        print("Submited weight: " + self.weightEdit.text() + "lbs.")

        # check to make sure user actually inputted some weight AND that its a float
        
        self.close_dialog()

    def close_dialog(self):
        print("Closing!")
        self.done(1)
