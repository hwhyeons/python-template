# zoom in / zoom out with mouse scroll

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

class CustomGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.zoom_factor = 1.0
        self.min_zoom_factor = 0.01
        self.max_zoom_factor = 100.0  # 100배 확대

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            delta = event.angleDelta().y() / 120.0
            scale_factor = 1.1 if delta > 0 else 0.9
            next_zoom_factor = self.zoom_factor * scale_factor
            if next_zoom_factor < self.min_zoom_factor or next_zoom_factor > self.max_zoom_factor:
                return
            self.zoom_factor *= scale_factor
            print(self.zoom_factor)
            self.scale(scale_factor, scale_factor)
        else:
            super().wheelEvent(event)

def main():
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    view = CustomGraphicsView()
    view.setScene(scene)

    for i in range(5):
        rect_item = QGraphicsRectItem(50 * i, 50 * i, 100, 50)
        rect_item.setBrush(QColor(Qt.red))
        scene.addItem(rect_item)

    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
