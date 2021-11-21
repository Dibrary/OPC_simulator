import sys, time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox

from PyQt5 import uic
from lxml import etree

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("slave_view.ui", self)
        self.setting()
        self.show()

    def setting(self): # xml파일 파싱을 자동으로 해 놓는 코드.
        root = (etree.parse("taglist.xml")).getroot()
        tag_group_count = []
        for idx, k in enumerate(root.iter()):
            if k.tag == "tag":
                tag_group_count.append(idx)
            if len(tag_group_count) == 2:
                break
        tag_count = tag_group_count[1]-tag_group_count[0]-1
        QMessageBox.information(self, "알림", str(tag_count))

        analyzer = []
        for country in root.iter("tag"):  # 우선 반복문을 통해 tag의 요소들을 '순서대로' 배열에 넣자.
            analyzer.append(country.findtext("analyzer"))
        QMessageBox.warning(self,"알림", str(analyzer)) # component 들어옴 확인.

app = QApplication([])
dialog = Main()
dialog.show()
app.exec_()