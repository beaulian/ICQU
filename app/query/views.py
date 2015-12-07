# coding=utf-8

import json
import redis
from . import query
from config import REDIS_URI, REDIS_PORT
from flask import request, make_response, session
from ..spiders.gradespider import GradeSpider
from ..spiders.libraryspider import LibrarySpider
from ..spiders.yikatongspider import YikatongSpider 


r0 = redis.Redis(host=REDIS_URI, port=REDIS_PORT, db=0)
r1 = redis.Redis(host=REDIS_URI, port=REDIS_PORT, db=1)
r2 = redis.Redis(host=REDIS_URI, port=REDIS_PORT, db=2)


@query.route("/library", methods=["GET"])
def library():
    # global SID, password
    SID = request.args.get("SID", "")
    password = request.args.get("password", "")
    sign = request.args.get("sign", "")
    if sign == "1":
        stripNumber = request.args.get("stripNumber")
        spider = LibrarySpider(SID, password)
        spider.post()
        tishi = spider.reRew(stripNumber)
        return make_response("<p align='center'>" + tishi + "</p>")

    if not r0.get("%s" % SID):
        spider = LibrarySpider(SID, password)
        spider.post()
        spider.main()
        if not spider.flag:
            wrong = {
                "errcode": 1,
                "errmsg": "wrong_id"
            }
            libraryJson = wrong
        else:
            libraryJson = spider.libraryJson
            r0.set("%s" % SID, libraryJson)
        r0.expire("%s" % SID, 21600)
    else:
        libraryJson = eval(r0.get("%s" % SID))

    resp = make_response(json.dumps(libraryJson), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-type'] = 'application/json'
    return resp


@query.route("/yikatong", methods=["GET"])
def yikatong():
    ySID = request.args["SID"]
    ypassword = request.args["password"]
    if not r1.get("%s" % ySID):
        spider = YikatongSpider(ySID, ypassword)
        spider.post()
        if not spider.flag:
            wrong = {
                "errcode": 1,
                "errmsg": "wrong_id"
            }
            yikatongJson = wrong
        else:
            yikatongJson = spider.result
            r1.set("%s" % ySID, yikatongJson)
            r1.expire("%s" % ySID, 7200)
    else:
        yikatongJson = eval(r1.get("%s" % ySID))

    resp = make_response(json.dumps(yikatongJson), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-type'] = 'application/json'
    return resp


@query.route("/getgrade", methods=["GET"])
def grade():
    gSID = request.args.get("SID")
    gpassword = request.args.get("password")
    year = request.args.get("year")
    team_number = request.args.get("team_number")
    if not r2.get("%s_%s_%s" % (gSID, year, team_number)):
        spider = GradeSpider(gSID, gpassword, year, team_number)
        spider.post()
        if not spider.flag:
            wrong = {
                "errcode": 1,
                "errmsg": "wrong SID or password"
            }
            gradeJson = wrong
        elif spider.error:
            wrong = {
                "errcode": 1,
                "errmsg": "cannot search"
            }
            gradeJson = wrong
        else:
            gradeJson = spider.grade_info
            r2.set("%s_%s_%s" % (gSID, year, team_number), gradeJson)
            r2.expire("%s_%s_%s" % (gSID, year, team_number), 43200)
    else:
        gradeJson = eval(r2.get("%s_%s_%s" % (gSID, year, team_number)))

    resp = make_response(json.dumps(gradeJson), 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-type'] = 'application/json'
    return resp
    

