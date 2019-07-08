""" Import  """
from PyQt4 import QtGui, uic

""" UI Class """
# load ui file for main layout
baseUIClass, baseUIWidget = uic.loadUiType("ui/weightDialog.ui")

# use loaded ui file in ui logic class
class WeightUILogic(baseUIWidget, baseUIClass):
    def __init__(self, parent=None):
        super(WeightUILogic, self).__init__(parent)
        self.setupUi(self)
