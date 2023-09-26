
import sys
import os
from PyQt5 import QtWidgets
from PyQt5 import uic

"""
예시
edit text 값 가져오기 : edit text의 이름이 et1이라면, self.ui.et1.toPlainText()
line edit 값 가져오기 : text()
"""
class MyApp(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        # ui 파일은 designer로 만들기
        self.ui = uic.loadUi("main.ui",self)
        self.ui.show()

    def event_function(self): # 만약 이벤트 Slot을 추가한 경우, 이런식으로 함수를 정의 필요
        pass


if __name__ == '__main__':
    # 모니터에따라 qt designer에서 나온 비율이랑 안맞을 수 있음
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    me = MyApp()
    sys.exit(app.exec()) # 화면 종료되면 프로그램 종료 -> 프로그램 종료 없이 하려면 app.exec() 단독 실행
