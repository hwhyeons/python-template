"""
23.12.20
Python 3.11 + Windows11 Insider Preview 231104-1132
발견된 오류 -> QApplication(sys.argv) 보다 QUiLoader() 문장이 뒤에 있으면 QUiLoader() 무한 루프
  - window = loader.load(ui_file) 위치도 QApplication보다 위에 있으면 무한 루프 걸림
  -> 이유는 모르고 순서 바꾸다가 된 코드가 아래 코드
"""
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

ui_file_name = "untitled.ui" # PyQt Designer로 만든 ui 파일
ui_file = QFile(ui_file_name)
# if not ui_file.open(QIODevice.ReadOnly):
#     print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
#     sys.exit(-1)
loader = QUiLoader()
app = QApplication(sys.argv)
window = loader.load(ui_file)
ui_file.close()
# if not window:
#     print(loader.errorString())
#     sys.exit(-1)
window.show()
sys.exit(app.exec())
