# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget , QLabel

from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import *
from pynput import mouse, keyboard
from ui_form import Ui_Widget
from Orc import Orc
from translate import *

#线程类
class New_Thread(QThread):
    finishSignal = Signal(str)
    img = 0;
    lang = 0;
    orc = Orc()
    def setImg(self,img,lang):
        self.img = img
        self.lang = lang

    def run(self):
        text = self.orc.image_to_string(self.img,self.lang)
        self.finishSignal.emit(text)



class Widget(QWidget):
    orc = Orc()
    seleWidget = 999;
    img = 0;
    flags = False
    startX =0
    startY = 0
    rectWidth = 0
    rectHeight = 0
    thread = New_Thread()
    translate = Translate();
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle("文字识别软件")
        self.setWindowOpacity(0.7)
        self.resize(700,200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ui.pushButton_seleRect.clicked.connect(self.on_Btn)
        self.ui.pushButton_rectOk.clicked.connect(self.on_BtnRectgOK)
        self.ui.plainTextEdit.setStyleSheet("color: red; font-size: 20px;")
        self.ui.pushButton_rectOk.setVisible(False)

        self.thread = self.thread
        self.thread.finishSignal.connect(self.UpdateText)

        #构造监听器对象,（鼠标监听哪几种类型事件）
        #listener = mouse.Listener(on_click=self.on_click)
        #listener.start()

        #键盘
        listenerKey = keyboard.Listener(
        on_press=self.on_press)
        # 监听启动：非阻断式
        listenerKey.start()
    # 点击监听 ,有bug暂时放弃
    def on_click(self,x, y, button, pressed):
        if (self.flags):
            if(x  >= self.startX and x <= self.startX + self.rectWidth
            and y >= self.startY and y <= self.startY +self.rectHeight):
                self.taskImg()


    def on_press(self,key):
        try:
            if(key.char == "q" and self.flags):
                self.taskImg()
        except AttributeError:
            return

    def taskImg(self):
        self.Camera(self.startX,self.startY,self.rectWidth,self.rectHeight)
        self.thread.setImg(self.img,"eng")
        self.thread.start()

    def on_BtnRectgOK(self):
        # 获取QWidget标题栏高度
        title_bar_height = self.frameGeometry().height() - self.geometry().height()
        point = self.seleWidget.pos()
        self.startX = point.x()
        self.startY = point.y() + title_bar_height
        self.rectWidth = self.width()
        self.rectHeight = self.height()

        # 获取当前窗口在哪个屏幕上
        #screen_number = QDesktopWidget().screenNumber(self)
      #  print("当前窗口在屏幕", screen_number, "上")

        self.ui.pushButton_rectOk.setVisible(False)
        self.seleWidget.close()
        self.flags = True


    def on_Btn(self):
        self.flags = False
        self.ui.pushButton_rectOk.setVisible(True)
        self.seleWidget = QWidget()
        self.seleWidget.setWindowOpacity(0.8)
        self.seleWidget.resize(700,200)
        self.seleWidget.setStyleSheet("background-color:transparent")
        self.seleWidget.move(20,20)
        self.seleWidget.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint)
        label = QLabel("以黑色区域为准,确定之后关闭窗口即可！", self.seleWidget)
        label.setStyleSheet("color: red;")
        label.move(700/2-50,200/2)
        self.seleWidget.show()

    def closeEvent(self, event):
        if (self.seleWidget != 999):
            self.flags = False
            self.seleWidget.close()

    def Camera(self,x,y,w,h):
        pixmap = QApplication.primaryScreen().grabWindow(0,x,y,w,h)
        self.img = self.orc.ImageFromQPixmap(pixmap)

    def UpdateText(self,text):
        newtext = self.translate.Totranslate(text,"en","zh")
        self.ui.plainTextEdit.setPlainText(newtext)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()

    sys.exit(app.exec())
