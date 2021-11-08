import ctypes
import inspect
import json
import time
import random
import time
import pymysql
import requests
from lxml import etree
from PySide2.QtCore import QFile, QObject, Signal
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTextBrowser, QPushButton, QSpinBox, QMessageBox
from threading import Thread

from common.SqlUtils import SQLManager


class MySignals(QObject):

    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(QTextBrowser, str)

    change_btn_name = Signal(QPushButton, str)

    change_spinBox_value = Signal(QSpinBox, int)


class MainUi:

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'cookie': 'f=n; commontopbar_new_city_info=172%7C%E5%8D%97%E4%BA%AC%7Cnj; commontopbar_ipcity=nj%7C%E5%8D%97%E4%BA%AC%7C0; id58=4ZrNcF7F7/oBi8dcKI91PA==; 58tj_uuid=5dfc8d6b-d40d-43e9-a860-b8f4485fe258; xxzl_deviceid=tcOuZy8YU6nLlYrX1cc7ZM4Hr%2BqG76d9UeEdf8nxxpgUClxe8ojdLkbrax%2B3iosw; gr_user_id=6930f4ea-e782-40cb-ad2f-2f120c955da3; als=0; wmda_uuid=2e828214a7cec0b6ec87dc872d7f5b3b; wmda_visited_projects=%3B11187958619315%3B2286118353409%3B1731916484865%3B6333604277682; city=sh; 58home=sh; ppStore_fingerprint=9332A99B86F9278740DC54983689CED9A5968F52A670F0B9%EF%BC%BF1636084412459; wmda_session_id_11187958619315=1636088816139-71972ae7-ade2-1389; utm_source=; new_uv=8; spm=; init_refer=https%253A%252F%252Fsh.58.com%252F; new_session=0; crmvip=""; dk_cookie=""; www58com="UserID=35010922549511&UserName=wqmd478"; 58cooper="userid=35010922549511&username=wqmd478"; 58uname=wqmd478; passportAccount="atype=0&bstate=0"; PPU=UID=35010922549511&UN=wqmd478&TT=749189e644c5ec820c22f4abbaca0a56&PBODY=T9QMVg4Noi2Kc22qw6iDkc7bS-8-j-i9F-RislrezCj-xF8KNXkNXsTjsqQH7Gw_YSSJIRR62DYFJS2xE8kdAsbkUIO4yIS56lb_eBQ2r50D18XTEbfdV6T5D9eZmM-dxiFrPGy1EBG3iLOqVX7Spwk-AC4MTxVUpuuAYHpHrMM&VER=1&CUID=Ws8961FjS9y4G5frUygB8w; xxzl_cid=b4e94f88e26144a6a367f6b412047282; xzuid=d0a3d003-ed93-48a0-8fc6-a56a9066941d; xxzl_smartid=94ce1c55e9b0e0df40d54c616b9d7c04'
    }

    city_list = ['全部']

    session = requests.Session()

    start_num = 1

    end_num = 10

    flag = False

    id_list = []

    def __init__(self):
        qFile = QFile("ui/spider.ui")
        qFile.open(QFile.ReadOnly)
        qFile.close()
        self.ui = QUiLoader().load(qFile)

        # 初始化选择框列表
        self.read_city()
        self.ui.urbanBox.addItems(self.city_list)

        # 发送信号
        self.ms = MySignals()
        self.ms.text_print.connect(self.print_to_gui)
        self.ms.change_btn_name.connect(self.change_button_text)
        self.ms.change_spinBox_value.connect(self.change_spinBox)

        # 按钮点击
        self.ui.urbanBtn.clicked.connect(self.spider_location)
        self.ui.hrefBtn.clicked.connect(self.spider_rent_href)
        self.ui.repeatBtn.clicked.connect(self.check_repeat_data)
        self.ui.deleteBtn.clicked.connect(self.delete_repeat_data)


    def print_to_gui(self, fb, text):
        fb.append(str(text))
        # fb.ensureCursorVisible()

    def change_button_text(self, fb, text):
        fb.setText(text)

    def change_spinBox(self, fb, value):
        fb.setValue(value)

    def read_city(self):
        db = SQLManager()
        cities = db.get_list('select name from city', [])
        db.close()
        for city in cities:
            self.city_list.append(city['name'])

    # 保存location表的数据
    def save_to_location(self, item):
        print(item)
        self.ms.text_print.emit(self.ui.urbanText, '地区名：' + item['r_name'])

    # 获取每个城市的地区
    def parse_area(self, response, item):
        x = etree.HTML(response.text)
        a_list = x.xpath('.//dl[@class="secitem secitem_fist"]/dd/a')
        print(len(a_list) - 1)
        self.ms.change_spinBox_value.emit(self.ui.totalBox, len(a_list) - 1)
        for a in a_list:
            href = a.xpath('./@href')[0]
            name = a.xpath('./text()')[0]
            if name != '不限':
                item['r_name'] = name
                item['url'] = href
                self.save_to_location(item)

    def spider_location(self):
        self.ui.urbanText.setText("")
        # 改变按钮的文本
        self.ui.urbanBtn.setText("结束爬取")
        # 拿到选举框中被选中的值
        selected_city = self.ui.urbanBox.currentText()
        if selected_city != '全部':
            db = SQLManager()
            city = db.get_one('select id, name, short_name from city where name = %s', [selected_city])
            db.close()
            def run():
                url = 'https://{}.58.com/chuzu/'.format
                item = {'c_id': city['id']}
                response = requests.get(url=url(city['short_name']), headers=self.headers)
                self.parse_area(response, item)
                self.ms.change_btn_name.emit(self.ui.urbanBtn, "开始爬取")
            t = Thread(target=run)
            t.start()
        else:
            QMessageBox.warning(
                self.ui,
                '警告',
                '暂时无法获取全部数据......')
            self.ui.urbanBtn.setText("开始爬取")

    t = []

    def save_to_house_url(self, item):
        print(item)
        # db = SQLManager()
        # sql = 'insert into house_url(url, r_id) values(%s, %s)'
        # db.modify(sql, item)
        # db.close()

    # 获取每页所有租房详情页的链接
    def parse_renting(self, response, r_id):
        count = 0
        x = etree.HTML(response.text)
        li_list = x.xpath('.//ul[@class="house-list"]/li')
        for li in li_list:
            href = li.xpath('./div[@class="des"]/h2/a/@href')
            if not href or 'https://' not in href[0]:
                continue
            count += 1
            self.save_to_house_url([href[0], r_id])
        self.ms.text_print.emit(self.ui.hrefText, '一共获取的到{}条链接数据'.format(count))
        self.ms.text_print.emit(self.ui.hrefText, '')
        time.sleep(random.randint(4, 7))

    # 获取每个地区所有页的租房信息
    def parse_href(self, href, r_id):
        self.ms.text_print.emit(self.ui.hrefText, "正在获取第{}页数据".format(self.start_num))
        response = self.session.get(url=href + '/pn{}'.format(self.start_num), headers=self.headers)
        self.parse_renting(response, r_id)

        while self.start_num < self.end_num:
            self.start_num += 1
            self.parse_href(href, r_id)

    def spider_rent_href(self):
        self.flag = not self.flag
        if self.flag:
            index = self.ui.indexBox.value()
            total = self.ui.totalBox.value()
            self.start_num = self.ui.startBox.value()
            self.end_num = self.ui.endBox.value()
            city = self.ui.urbanBox.currentText()
            self.ui.hrefText.setText("")
            # 改变按钮的文本
            self.ui.hrefBtn.setText("结束爬取")
            def run():
                db = SQLManager()
                if city == "全部":
                    location_list = db.get_list('select r_id, url, r_name  from location limit %s, %s', [index, total])
                else:
                    location_list = db.get_list('select r_id, url, r_name  from location where c_id = (select id from city where name=%s) limit %s, %s', [city, index, total])
                db.close()
                for location in location_list:
                    self.start_num = 1
                    self.ms.text_print.emit(self.ui.hrefText, '-------------------------------------------------------')
                    self.ms.text_print.emit(self.ui.hrefText, "正在获取{}地区的所有数据.........".format(location['r_name']))
                    self.ms.text_print.emit(self.ui.hrefText, '')
                    self.parse_href(location['url'], location['r_id'])
                    self.ms.text_print.emit(self.ui.hrefText, '-------------------------------------------------------')
                self.ms.change_btn_name.emit(self.ui.hrefBtn, "开始爬取")
            self.t.append(Thread(target=run))
            self.t[0].start()
        else:
            stop_thread(self.t[0])
            self.ms.text_print.emit(self.ui.hrefText, '结束运行！！！')
            QMessageBox.information(
                self.ui,
                '操作成功',
                '已经结束运行')
            self.ui.hrefBtn.setText("开始爬取")

    def check_repeat_data(self):
        self.id_list = []
        def run():
            db = SQLManager()
            r_id_list = db.get_list('select r_id from location', [])
            self.ui.repeatBar.setRange(0, len(r_id_list)-1)
            for k in range(0, len(r_id_list)):
                self.ui.repeatBar.setValue(k)
                url_list = db.get_list('select id, url from house_url where r_id=%s', [r_id_list[k]['r_id']])
                for i in range(0, len(url_list)):
                    house_id = url_list[i]['url'].split('?')[0].split('/')[-1].split('.')[0]
                    for j in range(i+1, len(url_list)):
                        if house_id in url_list[j]['url']:
                            self.id_list.append(url_list[j]['id'])
                            self.ms.text_print.emit(self.ui.repeatText, '{}有重复，当前索引位置为：{}'.format(house_id, url_list[j]['id']))
            db.close()
            if len(self.id_list) != 0:
                self.ms.text_print.emit(self.ui.repeatText, "一共有{}条数据是重复的！！！".format(len(self.id_list)))
            else:
                self.ms.text_print.emit(self.ui.repeatText, "没有重复的数据！！！")
        t = Thread(target=run)
        t.start()

    def delete_repeat_data(self):
        print(self.id_list)
        self.ui.repeatText.setText("")

        def run():
            db = SQLManager()
            for id in self.id_list:
                db.modify('delete from house_url where id=%s', id)
                self.ms.text_print.emit(self.ui.repeatText, "索引号：{},已被删除!!!".format(id))
            db.close()

            self.id_list = []
            self.ms.text_print.emit(self.ui.repeatText, "所有重复数据已被删除！！！")

        t = Thread(target=run)
        t.start()




def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def main():
    app = QApplication([])
    gui = MainUi()
    gui.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()
