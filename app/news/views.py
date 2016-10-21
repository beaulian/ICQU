# coding=utf-8

from config import MONGO_URI, MONGO_PORT, \
    GENERIC_MONGO_DB, JOB_MONGO_DB, ACADEMIC_MONGO_DB, \
    GENERIC_COLLECTION_NAME, JOB_COLLECTION_NAME, ACADEMIC_COLLECTION_NAME
from flask import Flask, render_template, current_app, g
from datetime import datetime
from pymongo import MongoClient
from functools import wraps
from . import news
import re


@news.before_request
def before_request():
    g.client = MongoClient(MONGO_URI, MONGO_PORT)    # 请求上下文的全局变量
    g.generic_news_info = []
    g.job_news_info = []
    g.academic_news_info = []
    g.regex = re.compile(r'<img[\s\S]+?src=\"(.*?)\"[\s\S]*>')


@news.teardown_request
def teardown_request(exception=None):
    g.client.close()


def get_news_info(prefix):
    def decorator(func):
        @wraps(func)
        def handler_args(*args, **kwargs):
            db = g.client[eval(prefix.upper() + "_MONGO_DB")]
            coll = db[eval(prefix.upper() + "_COLLECTION_NAME")]
            for new in coll.find().sort('recruit_time', -1):
                del new["_id"]
                if (prefix == "generic" or prefix == "academic"):
                    headimg = g.regex.findall(new["body"])
                    if not headimg:
                        new["headerimg"] = "/static/academicnews/head.jpg"
                    else:
                        new["headerimg"] = "http://news.cqu.edu.cn" + headimg[0]
                eval("g."+prefix+"_news_info").append(new)
	    key = "time_pub"
	    if prefix == "job":
		key = "recruit_time"
            eval("g."+prefix+"_news_info").sort(lambda y,x: cmp(datetime.strptime(x[key], "%Y-%m-%d"), datetime.strptime(y[key], "%Y-%m-%d")))
            eval("g."+prefix+"_news_info").append(len(eval("g."+prefix+"_news_info")))
            return func(*args, **kwargs)
        return handler_args
    return decorator


@news.route("/generic/page/<int:index>", methods=["GET"])
@get_news_info("generic")
def generic_news(index):
    # print len(g.generic_news_info)
    INDEX = int(index)
    START_PRE_PAGE = 0+10*INDEX
    END_PRE_PAGE = 10+10*INDEX
    count = g.generic_news_info[-1]
    if count < END_PRE_PAGE:
        END_PRE_PAGE = count
    return render_template("generic_news/news.html", news=g.generic_news_info[:-1], page=INDEX,
                           start=START_PRE_PAGE, end=END_PRE_PAGE, count=count)


@news.route("/job/page/<int:index>", methods=["GET"])
@get_news_info("job")
def job_news(index):
    INDEX = int(index)
    START_PRE_PAGE = 0+10*INDEX
    END_PRE_PAGE = 10+10*INDEX
    # print count
    count = g.job_news_info[-1]
    if count<END_PRE_PAGE:
        END_PRE_PAGE = count
    return render_template("job_news/jobnews.html", news=g.job_news_info[:-1], page=INDEX,
                           start=START_PRE_PAGE, end=END_PRE_PAGE, count=count)


@news.route("/academic/page/<int:index>", methods=["GET"])
@get_news_info("academic")
def academic_news(index):
    INDEX = int(index)
    START_PRE_PAGE = 0+10*INDEX
    END_PRE_PAGE = 10+10*INDEX
    count = g.academic_news_info[-1]
    if count<END_PRE_PAGE:
        END_PRE_PAGE = count
    return render_template("academic_news/academicnews.html", news=g.academic_news_info[:-1], page=INDEX,
                           start=START_PRE_PAGE, end=END_PRE_PAGE, count=count)


@news.route("/generic/page/info/<int:order>", methods=["GET"])
@get_news_info("generic")
def generic_info(order):
    real_order = int(order)-1
    return render_template("generic_news/careful_info.html", order=real_order, news=g.generic_news_info[:-1])


@news.route("/job/page/info/<int:order>", methods=["GET"])
@get_news_info("job")
def job_info(order):
    real_order = int(order)-1
    return render_template("job_news/jobinfo.html", order=real_order, news=g.job_news_info[:-1])


@news.route("/academic/page/info/<int:order>", methods=["GET"])
@get_news_info("academic")
def academic_info(order):
    real_order = int(order)-1
    return render_template("academic_news/careful_info.html", order=real_order, news=g.academic_news_info[:-1])
