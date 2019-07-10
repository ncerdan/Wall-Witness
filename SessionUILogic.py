""" Import  """
from PyQt4 import QtGui, uic

""" UI Class """
# load ui file for main layout
SessionDialogUI, SessionDialogBase = uic.loadUiType("ui/sessionDialog.ui")

# use loaded ui file in ui logic class
class SessionUILogic(SessionDialogBase, SessionDialogUI):
    def __init__(self, parent=None):
        super(SessionUILogic, self).__init__(parent)
        self.setupUi(self)
