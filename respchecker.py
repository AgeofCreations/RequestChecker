from ui import *
from PyQt5.Qt import *
import requests
#-------------------Обработка исключений--------------------------

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    quit()

    import sys
    sys.excepthook = log_uncaught_exceptions

#------------------Thread---------------------

class MyCheckUrlThread(QThread):
    about_check_url = pyqtSignal(str) #Проверка ответов
    good_requested_url = pyqtSignal(str) #Запись хороших ответов
    bad_requested_url = pyqtSignal(str) #Запись плохих ответов
    status_bar_info = pyqtSignal(int) #Контроль прогресс-бара
    lcd_value = pyqtSignal(int)
    def __init__(self, urls,state,repeats):
        super().__init__()
        self.state = state
        self.repeats = repeats
        self.urls = urls

#-------------Действия в потоке----------------

    def run(self):
        ir = 1
        if self.state == 1:
            self.repeats = 9999
        for ir in range(self.repeats):
            lcd_digit = ir + 1
            self.lcd_value.emit(lcd_digit)
            i = 1
            for url in self.urls:
                try:
                    shit = requests.get(url, allow_redirects=False)
                    code = shit.status_code
                except Exception as e:
                    # Пусть будет исключение
                    code = str(e)
                    self.bad_requested_url.emit('{}------{}'.format(url, code))

                self.about_check_url.emit('{}------{}'.format(url, code))

                zaluura = 99 / len(self.urls)

                if i <= 100:
                    i += zaluura
                    self.status_bar_info.emit(i)

                if code == 200:
                    self.good_requested_url.emit('{}------{}'.format(url, code))
                elif code == 307 or 301:
                    self.bad_requested_url.emit('{}------{}'.format(url, code))


#-------------------Объявление UI-----------------------

class MyWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.ui = Ui_RequestCheckerUI()
        self.ui.setupUi(self)
        self.urls = self.ui.textEdit
        self.barista = self.ui.CheckPB
        self.repeats = self.ui.spinBox
        self.lcd = self.ui.lcdNumber
        self.repeats.setValue(1)
        self.barista.setValue(0)

        self.result = self.ui.textEdit_2
        self.good = self.ui.textBrowser
        self.bad = self.ui.textBrowser_2

        self.ui.pushButton.clicked.connect(self._on_click_check)
        self.ui.pushButton_2.clicked.connect(self._erase_fields)

#----------------------Подключения к потоку---------------------------

        self.thread = MyCheckUrlThread(urls=None,state=0,repeats=1)
        self.thread.about_check_url.connect(self._on_about_check_url)
        self.thread.good_requested_url.connect(self._good_requested_url)
        self.thread.bad_requested_url.connect(self._bad_requested_url)
        self.thread.status_bar_info.connect(self._statusbarista)
        self.thread.lcd_value.connect(self._lcdfnc)
        self.thread.started.connect(self._buttconctrolstop)
        self.thread.finished.connect(self._butocnontrolstart)

#---------Функции интерфейса, выполняемые по сигналу из потока--------

    def _on_click_check(self):
        self.ui.textEdit_2.setText('')
        urls = self.urls.toPlainText().strip().split('\n')
        self.barista.setValue(0)
        repeats = self.repeats.value()
        self.thread.repeats = repeats
        self.thread.urls = urls
        self.thread.start()


    def _statusbarista(self,int):
        self.barista.setValue(int)


    def _on_about_check_url(self, text):
        self.result.append(text)

    def _good_requested_url(self, text):
        self.good.append(text)

    def _bad_requested_url(self,text):
        self.bad.append(text)

    def _lcdfnc(self,int):
        self.lcd.display(int)

    def _buttconctrolstop(self):
        self.ui.pushButton.setText('Стоп')
        self.ui.pushButton.clicked.connect(self.terminating_thread)
    def _butocnontrolstart(self):
        self.ui.pushButton.setText('Старт')
        self.ui.pushButton.clicked.connect(self.starting_thread)

    def terminating_thread(self):
        self.thread.terminate()

    def starting_thread(self):
        self.thread.start()


    def _erase_fields(self):
        self.ui.textBrowser.setText('')
        self.ui.textBrowser_2.setText('')
        self.ui.textEdit.setText('')
        self.ui.textEdit_2.setText('')

#-------------UI запуск------------------

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    myapp = MyWin()
    myapp.show()
    app.exec()

