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
        self.root = (etree.parse("taglist.xml")).getroot()
        self.setting()
        self.show()

    def count_calc(self): # xml파일 중에 실제 필요한 tag 내부의 태그 갯수 계산
        tag_group_count = []
        for idx, k in enumerate(self.root.iter()):
            if k.tag == "tag":
                tag_group_count.append(idx)
            if len(tag_group_count) == 2:
                break
        return tag_group_count[1]-tag_group_count[0]-1 # 19 나옴.

    def setting(self): # xml파일 파싱을 자동으로 해 놓는 코드.
        tag_count = self.count_calc()

        taggs = [[] for _ in range(0, tag_count)]

        analyzer = []
        for country in self.root.iter("tag"):  # 우선 반복문을 통해 tag의 요소들을 '순서대로' 배열에 넣자.
            analyzer.append(country.findtext("analyzer"))
        QMessageBox.warning(self,"알림", str(analyzer)) # component 들어옴 확인.

app = QApplication([])
dialog = Main()
dialog.show()
app.exec_()