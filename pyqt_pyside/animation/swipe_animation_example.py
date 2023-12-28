"""
참고 링크
https://stackoverflow.com/questions/25644026/setting-word-wrap-on-qlabel-breaks-size-constrains-for-the-window
"""

import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEasingCurve, QTimer, QElapsedTimer, QRect


class SlidingStackedWidget(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super(SlidingStackedWidget, self).__init__(parent)

        self.duration = 400 # 애니메이션 지속 시간 (단위 : ms)
        self.duration_bounce = 150 # 끝에 도달해서 살짝 튀는 애니메이션 지속 시간 (단위 : ms)
        self.m_direction = 'horizontal' # 애니메이션 진행 방향 (horizontal, vertical, diagonal) / QtCore.Qt.Horizontal
        self.animationType = QtCore.QEasingCurve.InOutQuad # Incurve, OutCurve, InOutQuad ...
        self.animation_bounce = QtCore.QEasingCurve.OutBounce # Incurve, OutCurve, InOutQuad ...
        self.circular = False  # 끝에 도달하면 처음으로 돌아가는지 여부

        # self.m_pnow = QtCore.QPoint(0, 0)
        self.m_active = False # active가 True면 애니메이션 진행중 -> 버튼 눌러도 동작 X
        self.move_right = False
        self.move_up = False
        self.is_bounce = False



    @QtCore.pyqtSlot()
    def slideInPrev(self):
        now = self.currentIndex()
        self.slideInIdx(now - 1)


    @QtCore.pyqtSlot()
    def slideInNext(self):
        now = self.currentIndex()
        self.slideInIdx(now + 1)


    def slideInIdx(self, idx):
        idx = idx % self.count()
        self.slideInWgt(self.widget(idx))


    def updateAnimation(self):
        elapsed = self.elapsedTimer.elapsed()
        duration = self.duration  # Total duration in milliseconds
        frame_width = self.frameRect().width()
        frame_height = self.frameRect().height()
        if elapsed > duration:
            self.timer.stop()
            self.m_active = False
            self.setCurrentIndex(self._next_idx)
            if self._now_idx != self._next_idx:
                self.widget(self._now_idx).hide()
            self.is_bounce = False
            return

        progress = elapsed / duration
        easedProgress = self.easingCurve.valueForProgress(progress)

        width_const = frame_width if not self.is_bounce else frame_width//4
        height_const = frame_height if not self.is_bounce else frame_height//4
        easedProgress_cal = None # bounce의 경우 추가 계산이 필요함
        if self.is_bounce and easedProgress >= 0.5:
            easedProgress_cal = 1 - easedProgress
        else:
            easedProgress_cal = easedProgress

        currentX = int(width_const*easedProgress_cal) if self.m_direction == 'horizontal' or self.m_direction == 'diagonal' else self.offset_X
        currentY = int(height_const*easedProgress_cal) if self.m_direction == 'vertical' or self.m_direction == 'diagonal' else self.offset_Y

        if self.m_direction == 'vertical':
            x_pos_next_move = currentX
            x_pos_now_move = currentX
        else:
            x_pos_next_move = frame_width - currentX if self.move_right else -frame_width + currentX
            x_pos_now_move = -currentX if self.move_right else currentX

        if self.m_direction == 'horizontal':
            y_pos_next_move = currentY
            y_pos_now_move = currentY
        else:
            y_pos_next_move = frame_height - currentY if self.move_up else -frame_height+currentY
            y_pos_now_move = -currentY if self.move_up else currentY

        if self._next_idx != self._now_idx:
            self.widget(self._next_idx).move(QtCore.QPoint(x_pos_next_move, y_pos_next_move))
            self.widget(self._next_idx).show()
            self.widget(self._next_idx).raise_()
        self.widget(self._now_idx).move(QtCore.QPoint(x_pos_now_move, y_pos_now_move))
        self.widget(self._now_idx).show()
        self.widget(self._now_idx).raise_()



    def slideInWgt(self, new_widget):
        # print("self.m_active : ", self.m_active)
        if self.m_active:
            return

        self.m_active = True

        _now = self.currentIndex()
        _next = self.indexOf(new_widget)


        if _now == _next:
            self.m_active = False
            return

        if abs(_now-_next) == self.count()-1 and not self.circular:
            self.is_bounce = True
            _next = _now
        # if _now == _next and not self.circular:
        #     self.is_bounce = True
        self._now_idx = _now
        self._next_idx = _next
        animation_type = self.animationType if not self.is_bounce else self.animation_bounce
        self.easingCurve = QEasingCurve(animation_type)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.elapsedTimer = QElapsedTimer()

        offset_X, offset_Y = self.frameRect().width(), self.frameRect().height()
        self.widget(_next).setGeometry(self.frameRect())

        if self.m_direction == 'horizontal':
            if _now < _next:
                if self.circular and abs(_next-_now) == self.count()-1:
                    self.move_right = False
                else:
                    self.move_right = True
            elif _now == _next and self.is_bounce and _now == 0:
                self.move_right = False
            elif _now == _next and self.is_bounce and _now == (self.count() - 1):
                self.move_right = True
            else:
                if self.circular and abs(_next-_now) == self.count()-1:
                    self.move_right = True
                else:
                    self.move_right = False
            offset_X = -offset_X
            offset_Y = 0
        elif self.m_direction == 'vertical':
            if _now < _next:
                if self.circular and abs(_next-_now) == self.count()-1:
                    self.move_up = False
                else:
                    self.move_up = True
            elif _now == _next and self.is_bounce and _now == 0:
                self.move_up = False
            elif _now == _next and self.is_bounce and _now == (self.count() - 1):
                self.move_up = True
            else:
                if self.circular and abs(_next-_now) == self.count()-1:
                    self.move_up = True
                else:
                    self.move_up = False
            offset_X, offset_Y = 0, -offset_Y
        elif self.m_direction == 'diagonal':
            if _now < _next:
                if self.circular and abs(_next-_now) == self.count()-1:
                    self.move_right = False
                    self.move_up = False
                else:
                    self.move_right = True
                    self.move_up = True
            elif _now == _next and self.is_bounce and _now == 0:
                self.move_right = False
                self.move_up = False
            elif _now == _next and self.is_bounce and _now == (self.count() - 1):
                self.move_right = True
                self.move_up = True
            else:
                if self.circular and abs(_next-_now) == self.count()-1:
                    self.move_right = True
                    self.move_up = True
                else:
                    self.move_right = False
                    self.move_up = False
            offset_X, offset_Y = -offset_X, -offset_Y
        else:
            raise Exception("잘못된 방향 값")

        self.offset_X = offset_X
        self.offset_Y = offset_Y

        self.elapsedTimer.start()
        self.timer.start(5)  # Update every 10 milliseconds



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        slidingStacked = SlidingStackedWidget()
        for i in range(4):
            label = QtWidgets.QLabel(
                f"label : {i} ", alignment=QtCore.Qt.AlignCenter
            )
            color = QtGui.QColor(*random.sample(range(255), 3))
            label.setStyleSheet(
                "QLabel{ background-color: %s; color : white; font: 40pt}"
                % (color.name(),)
            )
            slidingStacked.addWidget(label)

        button_prev = QtWidgets.QPushButton(
            "Previous", pressed=slidingStacked.slideInPrev
        )
        button_next = QtWidgets.QPushButton(
            "Next", pressed=slidingStacked.slideInNext
        )


        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget(button_prev)
        hlay.addWidget(button_next)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QVBoxLayout(central_widget)
        lay.addLayout(hlay)
        lay.addWidget(slidingStacked)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())
