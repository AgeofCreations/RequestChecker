
import sys
import threading
from Souce.ui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import Souce.worker
import urllib.request
import re
import time

def thread(reqCheck):
    #запуск функции во втором потоке
    def wrapper(*args,**kwargs):
        my_thread = threading.Thread(target=reqCheck, args=args,kwargs=kwargs)
        my_thread.start()
    return wrapper()

@thread
def processing(signal):
    #Имитация
    res = [i for i in 'hello']
    time.sleep(5)
    signal.emit(res)

    class MyWidget(QtWidgets.QWidget):
        processing = QtCore.pyqtSignal(list,name = 'signalOne')

        def __init__(self,parent = None):
            super(MyWidget, self).__init__(parent)
            self.mainLayout = QtWidgets.QHBoxLayout
            self.setLayout(self.mainLayout)

            self.button = QtWidgets.QPushButton("Emit ur signal",self)
            self.mainLayout.addWidget(self.button)
            #Запуск при нажатии
            self.ui.pushButton.clicked.connect(lambda: processing(self.signalOne))
            #Обработка сигнала
            self.signalOne.connect(self.mySignalHandler,QtCore.Qt.QueuedConnection)

        def mySignalHandler(selfself,data):
         print(data)

#--------------------------------------------------------------------------------------
#Объявление UI
class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_RequestCheckerUI()
        self.ui.setupUi(self)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.pushButton.clicked.connect(self.reqCheck)
#-------------------------------------------------------------------------------------
    #объявление функции, переменных, массива.
    def reqCheck(self):
        self.ui.textBrowser.setText("")
        self.ui.textBrowser_2.setText("")
        stroki = self.ui.textEdit.toPlainText()
        mas=stroki.split('\n')
        result_good=''
        result_bad=''
        #Цикл, который собирает и выводит ответы сервера
        for stroka in mas:
            url = (stroka)
            reqCode = urllib.request.urlopen(url).getcode()
            self.ui.textEdit_2.append(url)
            reqCodeStr3 = str(reqCode)
            self.ui.textEdit_2.append(reqCodeStr3)
            if reqCode == 200:
                reqCodeStr = str(reqCode)
                result_good = url+'------'+reqCodeStr+'\n'
                self.ui.textBrowser.append(result_good)
            elif reqCode == 301 or 302 or 303 or 304 or 305 or 300 or 400 or 401 or 402 or 403 or 404 or 405 or 500 or 501 or 502 or 503 or 504 or 505:
                reqCodeStr2 = str(reqCode)
                result_bad = url+'------'+reqCodeStr2+'\n'
                self.ui.textBrowser_2.append(result_bad)

#UI запуск
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())


