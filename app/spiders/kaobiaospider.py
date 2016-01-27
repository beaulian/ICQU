# coding=utf-8

import json
import requests

from hashlib import md5
from basespider import BaseSpider
from BeautifulSoup import BeautifulSoup


class KaobiaoSpider(BaseSpider):
    def __init__(self, SID, password):
        self.login_url =  "http://202.202.1.176:8080/_data/index_login.aspx"
        self.kaobiao_url = "http://202.202.1.176:8080/KSSW/stu_ksap_rpt.aspx"
        self.headers = {
                'Content-Type': 'application/x-www-form-urlencode',
                'Host': '202.202.1.176:8080',
                'Origin': 'http://202.202.1.176:8080',
                'Referer': 'http://202.202.1.176:8080/KSSW/stu_ksap.aspx'
        }
        self.hash_value = md5(SID+md5(password).hexdigest()[0:30].upper()+"10611").hexdigest()[0:30].upper()
        self.postdata = {
                    'txt_dsdsdsdjkjkjc': SID,
                    'txt_dsdfdfgfouyy': password,
                    'Sel_Type': 'STU',
                    '__VIEWSTATEGENERATOR': 'CAA0A5A7',
                    'efdfdfuuyyuuckjg': self.hash_value
        }
        self.postkaobiao = {
                'sel_xnxq': '20150',
                'sel_lc': '2015001,2015-2016学年第一学期集中考试周'.decode("utf-8").encode("gb2312"),
                'btn_search': "检索".decode("utf-8").encode("gb2312")
        }
        self.kaobiao = []
        super(KaobiaoSpider, self).__init__(SID, password)

    def post(self):
        s = requests.Session()
        r1 = s.post(self.login_url, data=self.postdata, headers=self.headers)
        r2 = s.post(self.kaobiao_url, data=self.postkaobiao, headers=self.headers)
        soup = BeautifulSoup(r2.text)
        td =soup("td")
        try:
            del td[11]
        except IndexError:
            self.flag = False
        kaobiao_type = td[0].text
        for key in range(3,len(td),8):
            self.kaobiao.append([x.text for x in td[key:key+8]])


if __name__ == '__main__':
    spider = KaobiaoSpider("学号", "密码")
    spider.post()
