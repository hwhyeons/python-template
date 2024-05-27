import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# ui_test_window를 ui파일에서 python 코드로 바꾼 py파일 경로를 불러오기
# QMainWindow가 아니라 QDialog의 경우에는 타입만 변경해주면 됨

from ui_test_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def actionTest(self):
        print("action test..")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
