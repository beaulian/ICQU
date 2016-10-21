# coding=utf-8

import requests

from basespider import BaseSpider
from BeautifulSoup import BeautifulSoup


class YikatongSpider(BaseSpider):
    def __init__(self, SID, password):

        self.login_url = "http://ids.cqu.edu.cn/amserver/UI/Login"
        self.kard_url = "http://i.cqu.edu.cn/welcome/getUserInfo.do"
        self.postdata = {
            "IDToken0": "",
            "IDToken1": SID,
            "IDToken2": password,
            "IDButton": "Submit",
            "goto": "",
            "encoded": "true",
            "gx_charset": "UTF-8"
        }
        self.result = []
        super(YikatongSpider, self).__init__(SID, password)

    def post(self):
        # print self.postdata
        s = requests.Session()    # 自动管理cookies
        req = s.post(self.login_url, data=self.postdata, headers=self.headers)
        req2 = s.get(self.kard_url, headers=self.headers)
        # print req2.text.encode("utf-8")
        soup = BeautifulSoup(req2.text)
        try:
            remainder1 = soup("td")[-5].text.split("元".decode("utf-8"))[0] + "元".decode("utf-8")
            penalty1 = soup("td")[-1].text.split("元".decode("utf-8"))[0] + "元".decode("utf-8")
        except IndexError:
            self.flag = False
            return
        self.result = [remainder1, penalty1]