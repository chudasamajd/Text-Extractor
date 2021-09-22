from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtCore,QtGui
import sys
import pyscreenshot
import pytesseract
import pyperclip

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(100,100,640,480)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog)

        self.setWindowState(Qt.WindowFullScreen)
        self.setStyleSheet("background-color:black")
        self.setWindowOpacity(0.5)

        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(),QtCore.QPoint()

    def paintEvent(self,event):
        paint = QtGui.QPainter(self)
        paint.setPen(QtGui.QPen(QtGui.QColor(255,255,255),3))
        paint.setBrush(QtGui.QColor(255,255,255,100))
        paint.drawRect(QtCore.QRect(self.start,self.end))

    def mousePressEvent(self,event):
        self.start = self.end = event.pos()
        self.update()

    def mouseMoveEvent(self,event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self,event):
        x1,x2 = sorted((self.start.x(),self.end.x()))
        y1,y2 = sorted((self.start.y(),self.end.y()))
        self.hide()
        img = pyscreenshot.grab(bbox=(x1,y1,x2,y2))
        extract_text(img)
        QApplication.quit()

def extract_text(image):
    data = pytesseract.image_to_string(image)
    pyperclip.copy(data)
    print(data)

app = QApplication(sys.argv)
gui = Gui()
gui.show()
sys.exit(app.exec_())
