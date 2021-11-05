import requests
from lxml import etree


class Spider:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'cookie': 'id58=c5/nfGFKDuylZmQONhZcAg==; 58tj_uuid=e24eea85-f69a-4916-ba2b-9275eccd9e7b; als=0; wmda_uuid=b4099ecd5c43dfc9106517313483a795; wmda_new_uuid=1; xxzl_deviceid=ksqwu%2F89dypu8Eltj%2F%2FvWeJUCNs%2FMbXB5hf6xK6vSKrsZxxth0QUtWaRQyoVfL%2Fe; wmda_visited_projects=%3B11187958619315%3B1731916484865; new_uv=2; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.google.com%252F; wmda_session_id_11187958619315=1635991061442-185d5bd1-2266-c804; new_session=0; city=nj; 58home=nj; ppStore_fingerprint=D7EAEC359473BAD5954A2B971A4B8D5345682EFC31C2558A%EF%BC%BF1635992795194; xxzl_cid=4d76ba0faeab478abe6e11b3acef86b6; xzuid=a213cfee-da81-49fa-8129-175b0b511a7e'
    }

    # city_list = ['nj', 'sh', 'su', 'hz', 'wx']

    city_list = ['nj']

    start_num = 1

    end_num = 2

    def parse_renting(self, response):
        print(response.text)
        # x = etree.HTML(response.text)


    def parse_href(self, href):
        print("正在获取第{}页数据".format(self.start_num))
        response = requests.get(url=href + '/pn{}'.format(self.start_num), headers=self.headers)
        self.parse_renting(response)

        while self.start_num < self.end_num:
            self.start_num += 1
            self.parse_href(href)

    # 保存location表的数据
    def save_to_location(self, item):
        print(item)

    # 获取每个城市的地区
    def parse_area(self, response, item):
        x = etree.HTML(response.text)
        a_list = x.xpath('.//dl[@class="secitem secitem_fist"]/dd/a')
        for a in a_list:
            href = a.xpath('./@href')[0]
            name = a.xpath('./text()')[0]
            item['r_name'] = name
            self.save_to_location(item)
            if name == '不限':
                self.parse_href(href)

    def run(self):
        url = 'https://{}.58.com/chuzu/'.format
        for i in range(len(self.city_list)):
            item = {'c_id': i + 1}
            print("开始获取{}城市的数据".format(self.city_list[i]))
            response = requests.get(url=url(self.city_list[i]), headers=self.headers)
            self.parse_area(response, item)


if __name__ == '__main__':
    spider = Spider()
    spider.run()