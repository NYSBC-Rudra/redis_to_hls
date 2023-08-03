import redis
from PIL import Image
from qtpy.QtGui import QImage, QPixmap
from qtpy import QtWidgets, QtGui, QtCore
from qtpy.QtCore import Qt
import sys
import numpy



#print(data)

# Convert the binary data to a file-like object
#data.encode()
#data = bytes.fromhex(data.replace('\\x', ''))
#print(data)
# Open the image using PIL



# Display the image
def getImage():
    r = redis.Redis(host = '127.0.0.1', port=6379)
    data = r.get('bzoom:RAW')   
    image = Image.frombuffer("RGB", (1224,1024), data)
    nparr_image = numpy.array(image)
    qt_image = QImage(image.tobytes(), 1224, 1024, QImage.Format_RGB888)
    return qt_image, nparr_image


# class MainWindow(QtWidgets.QWidget):

#     def __init__(self):
#         super().__init__()

#         self.label = QtWidgets.QLabel(self)
#         canvas = QtGui.QPixmap(1224, 1020)
#         canvas.fill(Qt.white)
#         self.label.setPixmap(canvas)
#         self.setCentralWidget(self.label)

#         self.last_x, self.last_y = None, None

#     def mouseMoveEvent(self, e):
#         if self.last_x is None: # First event.
#             self.last_x = e.x()
#             self.last_y = e.y()
#             return # Ignore the first time.

#         canvas = self.label.pixmap()
#         painter = QtGui.QPainter(canvas)
#         painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
#         painter.end()
#         self.label.setPixmap(canvas)

#         # Update the origin for next time.
#         self.last_x = e.x()
#         self.last_y = e.y()

#     def mouseReleaseEvent(self, e):
#         self.last_x = None
#         self.last_y = None


# app = QtWidgets.QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec_()

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'My Screen'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label = QtWidgets.QLabel(self)
        self.last_x, self.last_y = None, None
        canvas = QtGui.QPixmap(1224, 1020)
        self.label.setPixmap(canvas)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_image)
        timer.start(60*1000)
        self.update_image()

    def update_image(self):
        pixmap = QtGui.QPixmap(getImage())
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
            self.label.adjustSize()
            self.resize(pixmap.size())

    
    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.label.setPixmap(canvas)

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())



