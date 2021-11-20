import sys, time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication

from PyQt5 import uic

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("slave_view.ui", self)
        self.show()

app = QApplication([])
dialog = Main()
dialog.show()
app.exec_()