from Souce.ui import *
from PyQt5.Qt import *
import requests
import numpy as np
import concurrent.futures
import time
import asyncio
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

class MyAsyncCheckUrls(QThread):
    about_check_url = pyqtSignal(str)  # Проверка ответов
    good_requested_url = pyqtSignal(str)  # Запись хороших ответов
    bad_requested_url = pyqtSignal(str)  # Запись плохих ответов
    status_bar_info = pyqtSignal(int)  # Контроль прогресс-бара
    def __init__(self, working_list, working_list_2, working_list_3):
        super().__init__()
        self.urls = working_list
        self.urls2 = working_list_2
        self.urls3 = working_list_3
# -------------Действия в потоке----------------
    def run1(self):
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

    def run2(self):
        i = 1
        for url in self.urls2:
            try:
                shit = requests.get(url, allow_redirects=False)
                code = shit.status_code
            except Exception as e:
                # Пусть будет исключение
                code = str(e)
                self.bad_requested_url.emit('{}------{}'.format(url, code))

            self.about_check_url.emit('{}------{}'.format(url, code))

    async def run3(self):
        i = 1
        for url in self.urls3:
            try:
                shit = await requests.get(url, allow_redirects=False)
                code = await shit.status_code
            except Exception as e:
                # Пусть будет исключение
                code = str(e)
                self.bad_requested_url.emit('{}------{}'.format(url, code))

            self.about_check_url.emit('{}------{}'.format(url, code))

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(self.load_url())]
        wait_tasks = asyncio.wait(tasks)
        loop.run_until_complete(wait_tasks)
        loop.close()









"""

    def threading(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(MyAsyncCheckUrls.load_url, url, 60): url for url in self.urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                        data = future.result()
                except Exception as exc:
                           MyAsyncCheckUrls.load_url(url).shit.status_code = str(exc)
                else:
                    code = MyAsyncCheckUrls.load_url(url).shit.status_code
                    MyAsyncCheckUrls.about_check_url.emit('{}------{}'.format(url, code))
                    
"""








"""
            self.about_check_url.emit('{}------{}'.format(url, code))

            zaluura = 99 / len(self.urls)

            if i <= 100:
                i += zaluura
                self.status_bar_info.emit(i)

            if code == 200:
                self.good_requested_url.emit('{}------{}'.format(url, code))
            elif code == 307 or 301:
                self.bad_requested_url.emit('{}------{}'.format(url, code))
"""
"""

"""
#-------------------Объявление UI-----------------------

class MyWin(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.ui = Ui_RequestCheckerUI()
        self.ui.setupUi(self)
        self.urls = self.ui.textEdit
        self.barista = self.ui.CheckPB

        self.result = self.ui.textEdit_2
        self.good = self.ui.textBrowser
        self.bad = self.ui.textBrowser_2

        self.ui.pushButton.clicked.connect(self._on_click_check)
        self.ui.pushButton_2.clicked.connect(self._erase_fields)

#----------------------Подключения к потоку---------------------------

        self.thread = MyAsyncCheckUrls(working_list=None, working_list_2=None, working_list_3=None)
        self.thread.about_check_url.connect(self._on_about_check_url)
        self.thread.good_requested_url.connect(self._good_requested_url)
        self.thread.bad_requested_url.connect(self._bad_requested_url)
        self.thread.status_bar_info.connect(self._statusbarista)
        self.thread.started.connect(self._buttconctrolstop)
        self.thread.finished.connect(self._butocnontrolstart)

#---------Функции интерфейса, выполняемые по сигналу из потока--------

    def _on_click_check(self):
        self.ui.textEdit_2.setText('')
        urls = self.urls.toPlainText().strip().split('\n')
        part0, part1, part2 = np.array_split(urls, 3)
        my_String = '_'.join(part0)  # '' - разделитель между элементами списка соответственно
        my_String2 = '_'.join(part1)
        my_String3 = '_'.join(part2)
        self.ui.textEdit_Visual.setText(my_String)
        self.ui.textEdit_Visual_2.setText(my_String2)
        self.ui.textEdit_Visual_3.setText(my_String3)
        working_list = self.urls.toPlainText().strip().split('\n')
        working_list2 = self.urls.toPlainText().strip().split('\n')
        working_list3 = self.urls.toPlainText().strip().split('\n')
        self.barista.setValue(0)
        self.thread.working_list = working_list
        self.thread.working_list_2 = working_list2
        self.thread.working_list_3 = working_list3
        self.thread.start()


    def _statusbarista(self,int):
        self.barista.setValue(int)


    def _on_about_check_url(self, text):
        self.result.append(text)

    def _good_requested_url(self, text):
        self.good.append(text)

    def _bad_requested_url(self,text):
        self.bad.append(text)

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

