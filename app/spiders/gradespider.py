# coding=utf-8

import json
import requests

from hashlib import md5
from basespider import BaseSpider
from BeautifulSoup import BeautifulSoup


class GradeSpider(BaseSpider):
    def __init__(self, SID, password, year, team_number):

        self.login_url =  "http://202.202.1.176:8080/_data/index_login.aspx"
        # self.prefix_core_url = "http://202.202.1.176:8080/xscj/Stu_MyScore.aspx"
        self.core_url = "http://202.202.1.176:8080/xscj/Stu_MyScore_rpt.aspx"
        self.hash_value = md5(SID+md5(password).hexdigest()[0:30].upper()+"10611").hexdigest()[0:30].upper()
        self.postdata = {
                    'Sel_Type': 'STU',
                    'txt_dsdsdsdjkjkjc': SID,
                    'txt_dsdfdfgfouyy': password,
                    'txt_ysdsdsdskgf': "",
                    "pcInfo": "Mozilla%2F4.0+%28compatible%3B+MSIE+7.0%3B+Windows+NT+6.1%3B+Trident%2F7.0%3B+SLCC2%3B+.NET+CLR+2.0.50727%3B+.NET+CLR+3.5.30729%3B+.NET+CLR+3.0.30729%3B+Media+Center+PC+6.0%3B+.NET4.0C%29x860+SN%3ANULL",
                    "typeName": "%D1%A7%C9%FA",
                    "aerererdsdxcxdfgfg": "",
                    "efdfdfuuyyuuckjg": self.hash_value
        }
        self.postcore = {
                    "sel_xn": year,
                    "sel_xq": team_number,
                    "SJ": "0",
                    'btn_search':'%BC%EC%CB%F7',
                    "SelXNXQ": "2",
                    "zfx_flag": "0"
        }
        self.grade_info = {"课程总数":"","学年学期":"", "课程名称":[],"学分":[],"成绩":[]}
        self.error = False
        super(GradeSpider, self).__init__(SID, password)

    def post(self):
        s = requests.Session()
        req = s.post(self.login_url, data=self.postdata, headers=self.headers)
        # req2 = s.get(self.prefix_core_url, headers=self.headers)
        req2 = s.post(self.core_url, data=self.postcore, headers=self.headers)
        # print req2.text
        # return
        soup = BeautifulSoup(req2.text)
        try:
            td = soup("table")[-1]("td")
        except IndexError:
            self.error = True
            return
        self.grade_info["学年学期"] = td[0].text
        count = len(td)/11
        # print count
        self.grade_info["课程总数"] = count
        if count == 0:
            self.flag = False
            return

        for i in range(len(td)):
            if i % 10 == 1:
                self.grade_info["课程名称"].append(td[i].text)
<<<<<<< HEAD
            elif i % 10 == 2:
                self.grade_info["学分"].append(td[i].text)
            elif i % 10 == 6:
                self.grade_info["成绩"].append(td[i].text)
=======
                # print td[i].text
            elif i % 10 == 2:
                self.grade_info["学分"].append(td[i].text)
            elif i % 10 == 6:
                self.grade_info["成绩"].append(td[i].text)
>>>>>>> master
