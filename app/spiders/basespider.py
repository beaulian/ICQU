# coding=utf-8

# 基类也要指定object父类
# 所有类都必须要有继承的类,如果什么都不想继承，就继承到object类
class BaseSpider(object):
	def __init__(self, SID, password):

            self.SID = SID
            self.password = password
            self.flag = True   # 判断是否登录进去了
            self.headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, \
                                     like Gecko) Chrome/38.0.2125.122 Safari/537.36"
            }

            def __str__(self):
                return "yiban spider"

            def post(self):
                pass
