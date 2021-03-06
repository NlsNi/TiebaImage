import requests
import re
from bs4 import BeautifulSoup
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
import threading
import time
import random
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap


browser_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}
# http://tieba.baidu.com/p/4801622740 无图
# http://tieba.baidu.com/p/2491624899 有多页图
# http://tieba.baidu.com/p/2491624891 错误的帖子


class UI(QWidget):
    # labels
    _label_path = None
    _label_URL = None
    _label_log = None
    # buttons
    _button_explore = None
    _button_download = None
    # textboxes
    _text_path = None
    _text_URL = None
    _text_log = None
    # parameters
    _url = None
    _header = None
    _path = None
    # signal
    _clear_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._header = browser_header
        self.init_UI()

    def init_UI(self):

        self._label_path = QLabel('Path', self)
        self._label_URL = QLabel('URL', self)
        self._label_log = QLabel('Log', self)

        self._button_explore = QPushButton('Explore', self)
        self._button_download = QPushButton('Download', self)
        self._button_explore.setToolTip('Press this button to select the save path')
        self._button_explore.clicked.connect(self._action_explore)
        self._button_download.setToolTip('Press this button to download images')
        self._button_download.clicked.connect(self._action_download)

        self._text_path = QLineEdit(self)
        self._text_path.setToolTip('Enter the save path here')
        self._text_URL = QLineEdit(self)
        self._text_URL.setToolTip('Enter the Tieba URL here')
        self._text_log = QTextEdit(self)
        self._text_log.setToolTip('Logs are shown here')

        grid = QGridLayout(self)
        grid.setSpacing(10)

        grid.addWidget(self._label_path, 1, 0)
        grid.addWidget(self._text_path, 1, 1)
        grid.addWidget(self._button_explore, 1, 2)

        grid.addWidget(self._label_URL, 2, 0)
        grid.addWidget(self._text_URL, 2, 1)
        grid.addWidget(self._button_download, 2, 2)

        grid.addWidget(self._label_log, 3, 0)
        grid.addWidget(self._text_log, 3, 1, 5, 1)

        # 设置Icon 和背景图片
        icon = QIcon()
        # C++ reference
        # void QIcon::addPixmap(const QPixmap &pixmap, Mode mode = Normal, State state = Off)
        icon.addPixmap(QPixmap('icon.jpg'), mode=QIcon.Normal, state=QIcon.On)
        self.setWindowIcon(icon)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("bg.jpg")))
        self.setPalette(palette)

        self.setLayout(grid)
        self.setGeometry(500, 300, 400, 300)
        self.setWindowTitle('Tieba Image Downloader')
        self.show()

    # slot
    def _action_explore(self):
        path_name = QFileDialog.getExistingDirectory(self,"选择要保存到的文件夹", "C:/")
        self._text_path.setText(path_name)

    # slot
    def _action_download(self):
        self._path = self._text_path.text()
        self._url = self._text_URL.text()
        if len(self._path) == 0 or len(self._url) == 0:
            warning = QMessageBox.critical(self, "错误", "请补全Path和URL")
        else:
            self._path += r'/'
            thread_download = threading.Thread(target=self.download_image, name='th_download')
            thread_download.start()

    # slot
    def _action_clear_log(self):
        self._text_log.clear()

    def download_image(self):
        max_page = self._get_max_page()
        if max_page == '1':
            page_url = self._url
            self._get_image(page_url, 1)
        elif max_page is not None:
            for i in range(1, int(max_page) + 1):
                page_url = self._url + '?pn=' + str(i)
                self._get_image(page_url, str(i))

    def _get_max_page(self):
        try:
            response = requests.get(self._url, headers=self._header).content.decode('UTF-8')
            pattern = re.compile(r'共<span class="red">([0-9]*)</span>页')
            max_page = pattern.findall(response)[0]
            if max_page is not None:
                return max_page
        except IndexError:
            warning = QMessageBox.critical(self, "错误", "请输入有效的贴吧url")

    def _get_image(self, page_url, page):
        html = requests.get(page_url, headers=self._header).content.decode('UTF-8')
        soup = BeautifulSoup(html, 'lxml')
        pics = soup.find_all("img", {"class": "BDE_Image"})
        if len(pics) == 0:
            # 及时清空textEdit中的内容
            self._text_log.append("帖子当前页中未找到图片")
        else:
            for i in range(0, len(pics)):
                img_url = pics[i]['src']
                img = requests.get(img_url).content
                img_save_path = self._path + str(page)
                if os.path.exists(img_save_path):
                    pass
                else:
                    os.mkdir(img_save_path)
                with open(img_save_path + '/' + str(i) + ".jpg", 'wb') as f:
                    f.write(img)
                    # 利用PyQt的信号和槽机制让主线程清空 textEdit中的内容
                    # 防止子线程修改UI导致程序奔溃
                    if len(self._text_log.toPlainText()) >= 3000:
                        self._clear_signal.connect(self._action_clear_log)
                        self._clear_signal.emit()
                    self._text_log.append(img_url + ' saved')
                    t = random.randrange(1, 10)/10
                    time.sleep(t)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec())

