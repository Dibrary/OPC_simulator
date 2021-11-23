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

    def count_calc(self):
        '''
        xml파일 중에 실제 필요한 tag 내부의 태그 갯수 계산

        return : 반복되는 tag 갯수, (start, end)로 된 튜플
        '''
        tag_group_count = []
        for idx, k in enumerate(self.root.iter()):
            if k.tag == "tag":
                tag_group_count.append(idx)
            if len(tag_group_count) == 2:
                break
        return tag_group_count[1]-tag_group_count[0]-1, tag_group_count # 현재의 xml파일 기준으로 19 나옴.

    def tag_name_set(self, tag_group_count):
        '''
        xml파일 중에 실제 필요한 tag 내부의 태그 이름 담아서 반환
        
        tag_group_count : (start, end)로 된 튜플 
        return : tag_name이 들어있는 리스트
        '''
        tag_name_list = []
        for idx, v in enumerate(self.root.iter()):
            if idx == tag_group_count[1]:
                break
            if idx > tag_group_count[0]:
                tag_name_list.append(v.tag)
        return tag_name_list

    def setting(self): # xml파일 파싱을 자동으로 해 놓는 코드.
        tag_count, tag_group_count = self.count_calc()
        taggs = [[] for _ in range(0, tag_count)]
        tag_name_list = self.tag_name_set(tag_group_count)

        for idx, i in enumerate(tag_name_list): # 이 루프에서 tag들이 자동으로 들어간다.
            for node in self.root.iter("tag"):
                taggs[idx].append(node.findtext(i))

    def opc_server(self): # 서버 동작부는 따로 구현할 예정.

        return None


app = QApplication([])
dialog = Main()
dialog.show()
app.exec_()