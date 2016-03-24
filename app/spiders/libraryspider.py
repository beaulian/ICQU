# coding=utf-8

import json
import requests
import threading

from basespider import BaseSpider
from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup as Beautiful



class LibrarySpider(BaseSpider):

    def __init__(self, SID, password):

        self.response = None
        self.prefix_url = "http://lib.cqu.edu.cn"

        self.prefixUrl = "https://sso.lib.cqu.edu.cn:8949/adlibSso/login?service=http%3A%2F%2Flib.cqu.edu.cn%2Fmetro%2Findex.htm"
        self.firstUrl = "https://sso.lib.cqu.edu.cn:8949/adlibSso/login?service=http%3A%2F%2Flib.cqu.edu.cn%2Fmetro%2Flogin.htm"
        self.secondUrl = "http://lib.cqu.edu.cn/metro/login.htm"
        self.NowBorrowUrl = "http://lib.cqu.edu.cn/metro/readerNowBorrowInfo.htm"
        self.ReadBookingUrl = "http://lib.cqu.edu.cn/metro/readerBooking.htm"
        self.OutDateInfoUrl = "http://lib.cqu.edu.cn/metro/outDateInfo.htm"
        self.ReaderArrearageUrl = "http://lib.cqu.edu.cn/metro/readerArrearage.htm"

        self.headers = {
            'Host': 'sso.lib.cqu.edu.cn:8949',
            'Origin': 'https://sso.lib.cqu.edu.cn:8949',
            "Content-Type": "application/x-www-form-urlencoded",
            'Referer': 'https://sso.lib.cqu.edu.cn:8949/adlibSso/login',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, \
                                         like Gecko) Chrome/38.0.2125.122 Safari/537.36"
        }
        self.s = requests.Session()

        self.libraryJson = {"NowBorrow": {}, "ReadBooking": {}, "OutDateInfo": {}, "ReaderArrearage": {}}
        super(LibrarySpider, self).__init__(SID, password)

    def __str__(self):
        return "library spider"

    def get_args(self, url):
        try:
            response = self.s.get(url)
        except IOError as e:
            return e
        return response

    def analyze_args(self):
        resp = self.get_args(self.prefixUrl)
        soup = BeautifulSoup(resp.text, fromEncoding="gbk")
        inp = soup("input")
        lt = str(inp[3]).split('value="')[1].split('"')[0]
        execution = str(inp[4]).split('value="')[1].split('"')[0]
        return [lt, execution, resp.cookies]

    def post(self):
        args = self.analyze_args()
        lt = args[0]
        execution = args[1]
        postdata = {
            "username": self.SID,
            "password": self.password,
            "id": "null",
            "lt": lt,
            "execution": execution,
            "_eventId": "submit",
            "submit": "登录"
        }
        req = self.s.post(self.firstUrl, data=postdata, headers=self.headers)
        self.response = req

    def reRew(self, strnumber):
        req2 = self.s.get("http://lib.cqu.edu.cn/metro/renewbook.htm?stripNumber=%s" % strnumber)
        soup = Beautiful(req2.text)
        div = soup.find_all("div", attrs={"class": "tishi"})[0]
        tishi = div.find_all("p")[1].text
        return tishi

    def post_NowBorrow(self):
        req = self.s.get(self.NowBorrowUrl).text     # 不能乱传headers,最好不要有
        soup = Beautiful(req)
        if soup("p")[-1].text == "没有相关记录！".decode("utf-8"):
                self.libraryJson["NowBorrow"]["statusinfo"] = "none"
        else:
            try:
                table = soup.find_all("table", attrs={"class": "liebiao"})[0]
            except IndexError as e:
                self.flag = False
                return

            font = soup.find_all("font", attrs={"class": "redfont"})

            alreadyBorrow = font[0].text
            currentBorrow = font[2].text
            notComment = font[3].text
            sumBorrow = font[4].text
            self.libraryJson["NowBorrow"]["alreadyBorrow"] = alreadyBorrow
            self.libraryJson["NowBorrow"]["notComment"] = notComment
            self.libraryJson["NowBorrow"]["sumBorrow"] = sumBorrow
            self.libraryJson["NowBorrow"]["currentBorrow"] = currentBorrow

            tr = table.find_all("tr")
            th = tr[0].find_all("th")
            slen = len(th)

            for i in range(int(currentBorrow)):
                self.libraryJson["NowBorrow"]["book_%s" % str(i+1)] = {}
                td = tr[i+1].find_all("td")
                for j in range(slen):
                    if j == 0:
                        self.libraryJson["NowBorrow"]["book_%s" % str(i+1)][th[j].text.strip()] = self.prefix_url + td[j].img["src"]
                    elif j == 1:
                        self.libraryJson["NowBorrow"]["book_%s" % str(i+1)][th[j].text.strip()] = [self.prefix_url+td[j].a["href"], td[j].text]
                    elif j < 7:
                        self.libraryJson["NowBorrow"]["book_%s" % str(i+1)][th[j].text.strip()] = td[j].text
                    else:
                        self.libraryJson["NowBorrow"]["book_%s" % str(i+1)][th[j].text.strip()] = td[j].input["onclick"]

    def post_ReadBooking(self):
        req = self.s.get(self.ReadBookingUrl, cookies=self.response.cookies).text
        soup = Beautiful(req)

        if soup("p")[-1].text == "没有相关记录！".decode("utf-8"):
            self.libraryJson["ReadBooking"]["statusinfo"] = "none"
        else:
            try:
                table = soup.find_all("table", attrs={"class": "liebiao"})[0]
            except Exception as e:
                return e

            tr = table.find_all("tr")
            count_book = len(tr[1:])
            self.libraryJson["ReadBooking"]["count_book"] = str(count_book)
            th = tr[0].find_all("th")
            slen = len(th)

            for i in range(count_book):
                self.libraryJson["ReadBooking"]["book_%s" % str(i+1)] = {}
                td = tr[i+1].find_all("td")
                for j in range(1, slen):
                    if j == 1:
                        self.libraryJson["ReadBooking"]["book_%s" % str(i+1)][th[j].text.strip()] = self.prefix_url + td[j].img["src"]
                    elif j == 2:
                        self.libraryJson["ReadBooking"]["book_%s" % str(i+1)][th[j].text.strip()] = [self.prefix_url+td[j].a["href"], td[j].text]
                    else:
                        self.libraryJson["ReadBooking"]["book_%s" % str(i+1)][th[j].text.strip()] = td[j].text

    def post_OutDateInfo(self):
        req = self.s.get(self.OutDateInfoUrl, cookies=self.response.cookies).text
        soup = Beautiful(req)
        if soup("p")[-1].text == "没有相关记录！".decode("utf-8"):
            self.libraryJson["OutDateInfo"]["statusinfo"] = "none"
        else:
            try:
                table = soup.find_all("table", attrs={"class": "liebiao"})[0]
            except IndexError as e:
                return
            tr = table.find_all("tr")
            count_book = len(tr[1:])
            self.libraryJson["OutDateInfo"]["count_book"] = str(count_book)
            th = tr[0].find_all("th")
            slen = len(th)

            for i in range(count_book):
                self.libraryJson["OutDateInfo"]["book_%s" % str(i+1)] = {}
                td = tr[i+1].find_all("td")
                for j in range(slen):
                    if j == 0:
                        self.libraryJson["OutDateInfo"]["book_%s" % str(i+1)][th[j].text.strip()] = self.prefix_url + td[j].img["src"]
                    elif j == 1:
                        self.libraryJson["OutDateInfo"]["book_%s" % str(i+1)][th[j].text.strip()] = [self.prefix_url+td[j].a["href"], td[j].text]
                    else:
                        self.libraryJson["OutDateInfo"]["book_%s" % str(i+1)][th[j].text.strip()] = td[j].text

    def post_ReaderArrearage(self):
        req = self.s.get(self.ReaderArrearageUrl, cookies=self.response.cookies).text
        soup = Beautiful(req)
        if soup("p")[-1].text == "没有相关记录！".decode("utf-8"):
            self.libraryJson["ReaderArrearage"]["statusinfo"] = "none"
        else:
            try:
                table = soup.find_all("table", attrs={"class":"liebiao"})[0]
            except Exception as e:
                return

            font = soup.find_all("font",attrs={"class":"redfont"})[0].text
            self.libraryJson["ReaderArrearage"]["sumMoney"] = font

            tr = table.find_all("tr")
            count_book = len(tr[1:])
            self.libraryJson["ReaderArrearage"]["count_book"] = str(count_book)
            th = tr[0].find_all("th")
            slen = len(th)

            for i in range(count_book):
                self.libraryJson["ReaderArrearage"]["book_%s" % str(i+1)] = {}
                for j in range(slen):
                    td = tr[i+1].find_all("td")
                    self.libraryJson["ReaderArrearage"]["book_%s" % str(i+1)][th[j].text.strip()] = td[j].text

    def main(self):
        threads = []
        t1 = threading.Thread(target=self.post_NowBorrow)
        threads.append(t1)
        t2 = threading.Thread(target=self.post_ReadBooking)
        threads.append(t2)
        t3 = threading.Thread(target=self.post_OutDateInfo)
        threads.append(t3)
        t4 = threading.Thread(target=self.post_ReaderArrearage)
        threads.append(t4)

        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()
