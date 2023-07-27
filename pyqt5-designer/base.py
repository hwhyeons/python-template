
import sys
from PyQt5 import QtWidgets
from PyQt5 import uic

class MyApp(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        # ui 파일은 designer로 만들기
        self.ui = uic.loadUi("main.ui",self)
        self.ui.show()

    def event_function(self): # 만약 이벤트 Slot을 추가한 경우, 이런식으로 함수를 정의 필요
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    me = MyApp()
    sys.exit(app.exec())