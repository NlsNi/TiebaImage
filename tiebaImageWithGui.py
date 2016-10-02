import requests
import re
from bs4 import BeautifulSoup
import os
import sys
from PyQt5.QtWidgets import *


class TiebaImage:
    _url = None
    _header = None
    _path = None

    def __init__(self, url, header, path):
        self._url = url
        self._header = header
        self._path = path

    def download_image(self):
        max_page = self._get_max_page()
        if max_page == '1':
            page_url = self._url
            self._get_image(page_url, 1)
        elif max_page is not None:
            for i in range(1, int(max_page)):
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
            print("请输入有效的贴吧url")

    def _get_image(self, page_url, page):
        html = requests.get(page_url, headers=self._header).content.decode('UTF-8')
        soup = BeautifulSoup(html, 'lxml')
        pics = soup.find_all("img", {"class": "BDE_Image", "pic_type": "0"})
        if len(pics) == 0:
            print("帖子当前页中未找到图片")
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
                    print(img_url + ' saved')

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

    _label_path = None
    _label_URL = None
    _label_log = None

    _button_explore = None
    _button_download = None

    _text_path = None
    _text_URL = None
    _text_log = None

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self._label_path = QLabel('Path',self)
        self._label_URL = QLabel('URL',self)
        self._label_log = QLabel('Log',self)

        self._button_explore = QPushButton('Explore', self)
        self._button_download = QPushButton('Download', self)
        self._button_explore.clicked.connect(self._action_explore)
        self._button_download.clicked.connect(self._action_download)

        self._text_path = QLineEdit(self)
        self._text_URL = QLineEdit(self)
        self._text_log = QTextEdit(self)

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

        self.setLayout(grid)
        self.setGeometry(500, 300, 400, 300)
        self.setWindowTitle('Tieba Image Downloader')
        self.show()

    def _action_explore(self):
        path_name = QFileDialog.getExistingDirectory(self,"选择要保存到的文件夹","C:/")
        self._text_path.setText(path_name)

    def _action_download(self):
        save_path = self._text_path.text()
        tieba_url = self._text_URL.text()
        if len(save_path) == 0 or len(tieba_url) == 0:
            warning = QMessageBox.critical(self,"错误","请补全Path和URL")
        else:
            save_path += r'/'
            tiebaimage = TiebaImage(url=tieba_url, header=browser_header, path=save_path)
            tiebaimage.download_image()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec())

