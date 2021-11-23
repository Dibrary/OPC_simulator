import sys, time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox

from PyQt5 import uic
from lxml import etree
from opcua import Server


class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("slave_view.ui", self)
        self.root = (etree.parse("taglist.xml")).getroot()
        self.setting()

        self.server = Server()
        self.start_button.clicked.connect(lambda: self.start_opc_server())
        self.stop_button.clicked.connect(lambda: self.stop_opc_server())

        self.show()

    def count_calc(self):
        '''
        가상 xml파일 중에 실제 필요한 tag 내부의 태그 갯수 계산

        return : 반복되는 tag 갯수, (start, end)로 된 튜플
        (현재의 가상 xml파일 기준으로 19 가 tag 갯수다)
        '''
        tag_group_count = []
        for idx, k in enumerate(self.root.iter()):
            if k.tag == "tag":
                tag_group_count.append(idx)
            if len(tag_group_count) == 2:
                break
        return tag_group_count[1] - tag_group_count[0] - 1, tag_group_count

    def tag_name_get(self, tag_group_count):
        '''
        가상 xml파일 중에 실제 필요한 tag 내부의 태그 이름 담아서 반환

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

    def setting(self):
        '''
        xml파일 파싱을 자동으로 해 놓는 코드.

        가상 xml파일을 기준으로
        [['251-AH-001', '251-AH-002'],['1630AT155-NO', '1630AT255-NO'],['1630AT155-MO', '1630AT255-MO'],
         ['1630AT155-MR', '1630AT255-MR'],['1630AT155-RM', '1630AT255-RM'],['1630AT155-BD', '1630AT255-BD'],
         ['1630AT155-VO', '1630AT255-VO'],['1630AT155-SV', '1630AT255-SV'],['1630AT155-VR', '1630AT255-VR'],
         ['1630AT155-RV', '1630AT255-RV'],['1630AT155-VCR', '1630AT255-VCR'],['1630AT155-DSV', '1630AT255-DSV'],
         ['1630AT155-CB', '1630AT255-CB'],['1630AT155-XF', '1630AT255-XF'],['1630AT155-FA', '1630AT255-FA'],
         ['1630AT155-LB', '1630AT255-LB'],['1630AT155-LV', '1630AT255-LV'],['1630AT155-SA', '1630AT255-SA'],
         ['1630AT155', '1630AT255']]  꼴로 데이터가 들어간다.
        '''
        tag_count, tag_group_count = self.count_calc()
        taggs = [[] for _ in range(0, tag_count)]
        self.tag_name_list = self.tag_name_get(tag_group_count)

        for idx, i in enumerate(self.tag_name_list):  # 이 루프에서 tag들이 자동으로 들어간다.
            for node in self.root.iter("tag"):
                taggs[idx].append(node.findtext(i))

        self.taggs = taggs

    def server_url_get(self):
        URL = None
        for k in self.root.iter():
            if k.tag == "server":
                URL = k
                break
        return URL.findtext("url")

    def start_opc_server(self):  # 서버 동작부는 따로 구현할 예정.
        URL = self.server_url_get()
        QMessageBox.warning(self, "시작", "START 눌림")

        self.server.set_endpoint(URL)
        name = "OPCUA_SIMULATION_SERVER"
        addspace = self.server.register_namespace(name)
        node = self.server.get_objects_node()

        for idx, a in enumerate(self.taggs[0]):
            Param = node.add_object(addspace, a)
            for k in range(1, len(self.taggs)):
                tmp = Param.add_variable("ns=" + str(idx + 1) + "; s=" + self.taggs[k][idx], self.tag_name_list[k], 0)
                tmp.set_writable()
        self.server.start()
        return None

    def stop_opc_server(self):
        QMessageBox.warning(self, "시작", "STOP 눌림")
        self.server.stop()
        return None


app = QApplication([])
dialog = Main()
dialog.show()
app.exec_()