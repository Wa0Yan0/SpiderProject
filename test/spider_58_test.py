import random
import time

import requests
from lxml import etree

url = 'https://sh.58.com/chuzu/?PGTID=0d100000-0000-2084-226f-f3310a6f04c4&ClickID=2'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'cookie': 'id58=c5/nfGFKDuylZmQONhZcAg==; 58tj_uuid=e24eea85-f69a-4916-ba2b-9275eccd9e7b; als=0; wmda_uuid=b4099ecd5c43dfc9106517313483a795; wmda_new_uuid=1; xxzl_deviceid=ksqwu%2F89dypu8Eltj%2F%2FvWeJUCNs%2FMbXB5hf6xK6vSKrsZxxth0QUtWaRQyoVfL%2Fe; wmda_visited_projects=%3B11187958619315%3B1731916484865; new_uv=2; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.google.com%252F; wmda_session_id_11187958619315=1635991061442-185d5bd1-2266-c804; new_session=0; city=nj; 58home=nj; ppStore_fingerprint=D7EAEC359473BAD5954A2B971A4B8D5345682EFC31C2558A%EF%BC%BF1635992795194; xxzl_cid=4d76ba0faeab478abe6e11b3acef86b6; xzuid=a213cfee-da81-49fa-8129-175b0b511a7e'
}

if __name__ == '__main__':
    # response = requests.get(url=url, headers=headers)
    # x = etree.HTML(response.text)
    # li_list = x.xpath('.//ul[@class="house-list"]/li')
    # for li in li_list:
    #     href = li.xpath('./div[@class="des"]/h2/a/@href')
    #     if not href or 'https://' not in href[0]:
    #         continue
    #     response = requests.get(url=href[0], headers=headers)
    #     x = etree.HTML(response.text)
    #     title = x.xpath('.//div[@class="house-title"]/h1/text()')[0].strip()
    #     money = x.xpath('.//b[@class="f36 strongbox"]/text()')[0].strip()
    #     instructions = x.xpath('.//span[@class="instructions"]/text()')[0].strip()
    #     print(title, money, instructions)
    #     time.sleep(random.randint(4, 7))
    url = 'https://nj.58.com/zufang/47359720149689x.shtml?houseId=2140002495110152&shangquan=bjhnj&shangquanId=32326&dataSource=2&tid=b19e580d-8189-44d4-8775-acc91f65cf46&legourl=//legoclick.58.com/jump?target=szq8pB3draOWUvYfXMRhmyOMs1ELn1NOP1cknHEOPW9OXaO1pZwVUT7bsHFWnh7bnvN1sHF6mHcVPAmdmBY3m1mYsycQnWEvrARWmHEQuTD3nj9YnH9zP1DYPj0YrTDKnWDYnjTknWEOPHDQnjDdn9DQnjbknTDQnjbknTDQsjDkTHDLnBkzrHmdTHDvn1mkrHELPjnYnjTKnWmKwbnVNDnVOlXxOCB4OsBeOmBgl2AClpAdOGyYOuacOlXxOoXLOCliTHDKnEDKsHDKTHDYPHm1njDLPHT1nHEkrjc1njEKP9DKnE76mhE1mHEOmzYQuWI-sHEvmWmVmynQPidWPhN1myNznH9QnjbKnHEdPWnknH0dnjELP1mvnjDvnTDQPjNvn1TQP1Nkn19dn19dPj0zTEDQsjDkTEDKTiYKTEDKTHN3sWcQnz3OsWNkTHTKnTDKnikQnE7exEDQnjT1nkDQnjTQPHTvTycQryNdrjKbsH9QrjbVPjwbPaY3P10dsy7Wm1bQuWmdmvmYP9DKnTDKTHTKnH0zsjcOPWN_n1c1nWmKnE78IyQ_Ty7bPH76uWRbuHDOrHI6ujc&referinfo=1'
    house_id = url.split('?')[0].split('/')[-1].split('.')[0]
    if house_id not in url:
        print(house_id)
    else:
        print("已经存在")