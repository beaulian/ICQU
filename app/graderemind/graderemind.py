# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../")

import re
import redis
from mail import send_mail
from config import REDIS_URI, REDIS_PORT
from spiders.gradespider import GradeSpider


r3 = redis.Redis(host=REDIS_URI, port=REDIS_PORT, db=3)

def get_subject_exist():
	subject_exist_set = r3.smembers("subject_exist")
	return subject_exist_set


def set_subject_exist(subject):
	r3.sadd("subject_exist", subject)


def send_grade_info(mail_receiver, year, team):
	spider = GradeSpider(sys.argv[1], sys.argv[2], year, team)
	spider.post()
	grade_info = spider.grade_info
	grade_subject = grade_info["课程名称"]
	grade_score = grade_info["成绩"]
	info = dict(zip(grade_subject, grade_score))
	
	grade = {}
	for subject, score in info.iteritems():
		if re.search("\d+\.\d+", score) and subject not in list(get_subject_exist()):
			set_subject_exist(subject)
			grade[subject] = score
	if grade:
		prefix_str = "新出来的成绩如下:  \n\n"
		content_str = "\n\n".join(["课程名称为: " + subject +
						 "\n成绩为: " + score for subject, score in grade.iteritems()])
		send_mail(prefix_str + content_str, mail_receiver)


send_grade_info("gjw.jesus@qq.com", "2015", "0")
            	



