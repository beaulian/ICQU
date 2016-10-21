# coding=utf-8

import json
import requests

from basespider import BaseSpider


class KebiaoSpider(BaseSpider):
    def __init__(self, SID, password):

        self.slogin_url = "http://syjx.cqu.edu.cn/login"
        self.skebiao_url = "http://syjx.cqu.edu.cn/admin/schedule/getPrintStudentSchedule"
        self.postdata = {
            "username": SID,
            "password": md5(password).hexdigest()
        }
        self.postdata2 = {
            "stuNum": SID
        }
        self.sresult = {}
        super(KebiaoSpider, self).__init__(SID, password)

    def post(self):
        s = requests.Session()
        req = s.post(self.slogin_url, data=self.postdata, headers=self.headers)
        req2 = s.post(self.skebiao_url, data=self.postdata2, headers=self.headers)
        if not req2.text:
            self.flag = False
            return
        self.sresult = json.loads(req2.text)