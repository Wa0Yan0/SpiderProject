import random
import time
import pymysql
import requests
from lxml import etree

MYSQL = {
    'host': '47.102.139.195',
    'port': 3306,
    'user': 'root',
    'passwd': 'root',
    'db': 'jobseeker_post',
    'charset': 'utf8',
}


class SQLManager(object):

    # 初始化实例方法
    def __init__(self):
        """

        :rtype: object
        """
        self.conn = None
        self.cursor = None
        self.connect()

    # 连接数据库
    def connect(self):
        self.conn = pymysql.connect(
            host=MYSQL['host'],
            port=MYSQL['port'],
            user=MYSQL['user'],
            passwd=MYSQL['passwd'],
            db=MYSQL['db'],
            charset=MYSQL['charset']
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询一条数据
    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        return self.cursor.fetchone()

    # 查询所有数据
    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        return self.cursor.fetchall()

    # 修改数据
    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 批量修改数据
    def multi_modify(self, sql, args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    # 关闭所有连接
    def close(self):
        self.cursor.close()
        self.conn.close()


class SpiderLocation:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'cookie': 'f=n; commontopbar_new_city_info=172%7C%E5%8D%97%E4%BA%AC%7Cnj; commontopbar_ipcity=nj%7C%E5%8D%97%E4%BA%AC%7C0; id58=4ZrNcF7F7/oBi8dcKI91PA==; 58tj_uuid=5dfc8d6b-d40d-43e9-a860-b8f4485fe258; xxzl_deviceid=tcOuZy8YU6nLlYrX1cc7ZM4Hr%2BqG76d9UeEdf8nxxpgUClxe8ojdLkbrax%2B3iosw; gr_user_id=6930f4ea-e782-40cb-ad2f-2f120c955da3; als=0; wmda_uuid=2e828214a7cec0b6ec87dc872d7f5b3b; wmda_visited_projects=%3B11187958619315%3B2286118353409%3B1731916484865%3B6333604277682; city=sh; 58home=sh; ppStore_fingerprint=9332A99B86F9278740DC54983689CED9A5968F52A670F0B9%EF%BC%BF1636084412459; wmda_session_id_11187958619315=1636088816139-71972ae7-ade2-1389; utm_source=; new_uv=8; spm=; init_refer=https%253A%252F%252Fsh.58.com%252F; new_session=0; crmvip=""; dk_cookie=""; www58com="UserID=35010922549511&UserName=wqmd478"; 58cooper="userid=35010922549511&username=wqmd478"; 58uname=wqmd478; passportAccount="atype=0&bstate=0"; PPU=UID=35010922549511&UN=wqmd478&TT=749189e644c5ec820c22f4abbaca0a56&PBODY=T9QMVg4Noi2Kc22qw6iDkc7bS-8-j-i9F-RislrezCj-xF8KNXkNXsTjsqQH7Gw_YSSJIRR62DYFJS2xE8kdAsbkUIO4yIS56lb_eBQ2r50D18XTEbfdV6T5D9eZmM-dxiFrPGy1EBG3iLOqVX7Spwk-AC4MTxVUpuuAYHpHrMM&VER=1&CUID=Ws8961FjS9y4G5frUygB8w; xxzl_cid=b4e94f88e26144a6a367f6b412047282; xzuid=d0a3d003-ed93-48a0-8fc6-a56a9066941d; xxzl_smartid=94ce1c55e9b0e0df40d54c616b9d7c04'
    }

    city_list = ['nj', 'sh', 'su', 'hz', 'wx']

    # 保存location表的数据
    def save_to_location(self, item):
        print(item)
        # db = SQLManager()
        # sql = 'insert into location(r_name, c_id, url) values(%s, %s, %s)'
        # db.modify(sql, [item['r_name'], item['c_id'], item['url']])
        # db.close()

    # 获取每个城市的地区
    def parse_area(self, response, item):
        x = etree.HTML(response.text)
        a_list = x.xpath('.//dl[@class="secitem secitem_fist"]/dd/a')
        for a in a_list:
            href = a.xpath('./@href')[0]
            name = a.xpath('./text()')[0]
            if name != '不限':
                item['r_name'] = name
                item['url'] = href
                self.save_to_location(item)

    def run(self):
        url = 'https://{}.58.com/chuzu/'.format
        for i in range(len(self.city_list)):
            item = {'c_id': i + 1}
            print("开始获取{}城市的数据".format(self.city_list[i]))
            response = requests.get(url=url(self.city_list[i]), headers=self.headers)
            self.parse_area(response, item)


class SpiderHouseURL:

    session = requests.Session()

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'cookie': 'f=n; commontopbar_new_city_info=172%7C%E5%8D%97%E4%BA%AC%7Cnj; commontopbar_ipcity=nj%7C%E5%8D%97%E4%BA%AC%7C0; id58=4ZrNcF7F7/oBi8dcKI91PA==; 58tj_uuid=5dfc8d6b-d40d-43e9-a860-b8f4485fe258; xxzl_deviceid=tcOuZy8YU6nLlYrX1cc7ZM4Hr%2BqG76d9UeEdf8nxxpgUClxe8ojdLkbrax%2B3iosw; gr_user_id=6930f4ea-e782-40cb-ad2f-2f120c955da3; als=0; wmda_uuid=2e828214a7cec0b6ec87dc872d7f5b3b; wmda_visited_projects=%3B11187958619315%3B2286118353409%3B1731916484865%3B6333604277682; city=sh; 58home=sh; ppStore_fingerprint=9332A99B86F9278740DC54983689CED9A5968F52A670F0B9%EF%BC%BF1636084412459; crmvip=""; dk_cookie=""; www58com="UserID=35010922549511&UserName=wqmd478"; 58cooper="userid=35010922549511&username=wqmd478"; 58uname=wqmd478; passportAccount="atype=0&bstate=0"; xxzl_smartid=94ce1c55e9b0e0df40d54c616b9d7c04; f=n; xxzl_cid=b4e94f88e26144a6a367f6b412047282; xzuid=d0a3d003-ed93-48a0-8fc6-a56a9066941d; PPU=UID=35010922549511&UN=wqmd478&TT=749189e644c5ec820c22f4abbaca0a56&PBODY=b3s0GgXj0CSjXo7uKEBabLWwJrLk3r5ut52ALbXbLfG5Bd0H1AHGQoZSlhas6ik5Ghme5pGLuytyJaHhAezOGfu54IZZLHusCBV489yMedAJdniLZZtC6yDMbJHK9zXPGjgjgSw_N-pvI5VpynT7-xT4-YAy3VTiBla4bCyH1zM&VER=1&CUID=Ws8961FjS9y4G5frUygB8w; wmda_session_id_11187958619315=1636093887015-243fb52b-22b9-3190; new_uv=9; utm_source=; spm=; init_refer=; new_session=0'
    }

    start_num = 1

    end_num = 10

    # 解析租房的详情页信息
    def parse_house(self, response):
        # response = requests.get(url=href[0], headers=self.headers)
        # self.parse_house(response)
        x = etree.HTML(response.text)

    def save_to_house_url(self, item):
        print(item)
        db = SQLManager()
        sql = 'insert into house_url(url, r_id) values(%s, %s)'
        db.modify(sql, item)
        db.close()

    # 获取每页所有租房详情页的链接
    def parse_renting(self, response, r_id):
        x = etree.HTML(response.text)
        li_list = x.xpath('.//ul[@class="house-list"]/li')
        for li in li_list:
            href = li.xpath('./div[@class="des"]/h2/a/@href')
            if not href or 'https://' not in href[0]:
                continue
            self.save_to_house_url([href[0], r_id])
        time.sleep(random.randint(4, 7))

    # 获取每个地区所有页的租房信息
    def parse_href(self, href, r_id):
        print("正在获取第{}页数据".format(self.start_num))
        response = self.session.get(url=href + '/pn{}'.format(self.start_num), headers=self.headers)
        self.parse_renting(response, r_id)

        while self.start_num < self.end_num:
            self.start_num += 1
            self.parse_href(href, r_id)

    def run(self):
        db = SQLManager()
        location_list = db.get_list('select r_id, url, r_name  from location limit %s, %s', [58, 10])
        db.close()
        for location in location_list:
            self.start_num = 1
            print('-------------------------------------------------------')
            print("正在获取{}地区的所有数据".format(location['r_name']), location['url'])
            self.parse_href(location['url'], location['r_id'])
            print('-------------------------------------------------------')

if __name__ == '__main__':
    spider = SpiderHouseURL()
    spider.run()